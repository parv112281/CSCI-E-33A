document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', () => compose_email(null));

  // handle new email submission
  document.querySelector('#compose-form').onsubmit = submit_email;

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email(email = null) {
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email-detail-view').style.display = 'none';

  // set to blank if this function is not called with email,
  // otherwise set to values from email
  const recipients = (email === null) ? '' : email.sender;
  let subject = '';
  let body = '';
  if(email !== null && email !== undefined) {
    if (email.subject.startsWith('Re:')) {
      subject = email.subject;
    } else {
      subject = `Re: ${email.subject}`;
    }
    body = `On ${email.timestamp} ${email.sender} wrote:\n${email.body}`
  }
  
  // Clear out composition fields
  document.querySelector('#compose-recipients').value = recipients;
  document.querySelector('#compose-subject').value = subject;
  document.querySelector('#compose-body').value = body;
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-detail-view').style.display = 'none';

  // load emails
  load_emails(mailbox);

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
}

function load_emails(mailbox) {
  fetch('/emails/' + mailbox)
  .then(response => response.json())
  .then(emails => {
      // Print emails
      console.log(emails);

      // create container for each email
      emails.forEach(email => {
        // top level container for email line
        const email_div = document.createElement('div');
        email_div.classList.add('row');
        email_div.classList.add('email');
        if (email.read) {
          email_div.classList.add('read_email');
        }
        
        // from 
        const from_div = document.createElement('div');
        from_div.classList.add('col-md-3');
        from_div.innerHTML = email.sender;
        email_div.append(from_div);

        // subject 
        const subject_div = document.createElement('div');
        subject_div.classList.add('col-md-6');
        subject_div.innerHTML = email.subject;
        email_div.append(subject_div);

        // timestamp
        const date_div = document.createElement('div');
        date_div.classList.add('col-md-3');
        date_div.innerHTML = email.timestamp;
        email_div.append(date_div);

        // handle email click
        email_div.addEventListener('click', function() {
            console.log(`Email with id ${email.id} has been clicked.`)
            load_email_view(email.id, mailbox);
        });

        document.querySelector('#emails-view').append(email_div);
      });
  });
}

function load_email_view(email_id, source) {
  fetch('/emails/' + email_id)
  .then(response => response.json())
  .then(email => {
      // Print email
      console.log(email);

      // display single email view, hide the others
      document.querySelector('#emails-view').style.display = 'none';
      document.querySelector('#compose-view').style.display = 'none';
      document.querySelector('#email-detail-view').style.display = 'block';

      // fetch email div
      const email_view = document.querySelector('#email-detail-view');
      email_view.innerHTML = '';

      const email_header = document.createElement('p');
      email_header.classList.add('email_header');

      // create From line
      const from = document.createElement('div');
      from.classList.add('row');
      from.innerHTML = `From: ${email.sender}`;
      email_header.append(from);

      // create To line
      const to = document.createElement('div');
      to.classList.add('row');
      to.innerHTML = `To: ${email.recipients.toString()}`;
      email_header.append(to);

      // create Subject line
      const subject = document.createElement('div');
      subject.classList.add('row');
      subject.innerHTML = `Subject: ${email.subject}`;
      email_header.append(subject);

      // create Timestamp line
      const timestamp = document.createElement('div');
      timestamp.classList.add('row');
      timestamp.innerHTML = `Timestamp: ${email.timestamp}`;
      email_header.append(timestamp);

      email_view.append(email_header);

      // create Reply button line
      const replyButton = document.createElement('button');
      replyButton.classList.add('btn');
      replyButton.classList.add('btn-sm');
      replyButton.classList.add('btn-outline-primary');
      replyButton.textContent = 'Reply'
      replyButton.onclick = () => compose_email(email);
      email_view.append(replyButton);

      // Archive and Unarchive button definition
      if(source === 'inbox' || source === 'archive') {
        const arcButton = document.createElement('button');
        arcButton.classList.add('btn');
        arcButton.classList.add('btn-sm');
        arcButton.classList.add('btn-outline-primary');
        arcButton.textContent = (source === 'inbox') ? 'Archive' : 'Unarchive';
        arcButton.onclick = () => handle_archiving(email.id, source === 'inbox')
        email_view.append(arcButton);
      } else {
        // sent box does not need an archive or unarchive button
      }

      email_view.append(document.createElement('hr'));

      // create Body
      const email_body = document.createElement('p');
      email_body.innerHTML = email.body;
      email_view.append(email_body);

      // mark email as read
      fetch('/emails/' + email_id, {
        method: 'PUT',
        body: JSON.stringify({
            read: true
        })
      });
  });
}

function handle_archiving(email_id, isArchived) {
  // if isArchived is true, email gets archived, otherwise it is unarchived
  fetch('/emails/' + email_id, {
    method: 'PUT',
    body: JSON.stringify({
        archived: isArchived
    })
  })
  .then(response => {
    console.log(response);
    load_mailbox('inbox');
  });  
}

function submit_email() {
  // POST request when email is submitted
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: document.querySelector('#compose-recipients').value,
        subject: document.querySelector('#compose-subject').value,
        body: document.querySelector('#compose-body').value
    })
  })
  .then(response => response.json())
  .then(result => {
      // Print result
      console.log(result);
      load_mailbox('sent');
  });
  return false;
}