
class MyColorScheme {
    constructor(epitopes) {
        this.epitopes = epitopes;
        this.index = 0;
        this.epitopes_ptrs = []
        this.iter_length = epitopes.length * 10;
        for (let i = 0; i < epitopes.length; i++) {
            this.epitopes_ptrs.push(0);
        }

    }

    getColor(element) {
        const iter = Math.floor(this.index / this.iter_length);
        const iter_idx = this.index % this.iter_length;
        const epitopes_idx = Math.floor(iter_idx / 10);
        const res_idx = (iter * 10) + (iter_idx % 10);
        this.index++;

        if (this.epitopes[epitopes_idx].length > this.epitopes_ptrs[epitopes_idx]) {
            if ((this.epitopes[epitopes_idx][this.epitopes_ptrs[epitopes_idx]] - 1) === res_idx) {
                this.epitopes_ptrs[epitopes_idx]++;
                return "red";
            }
        }
        return "white";
    }
}

class FileUpload extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            patentIds: 'US8829165B2,US8563698B2',
            displaySearch: true,
            result: {}
        };
    }

    resetState = () => {
        this.setState({
            patentIds: 'US8829165B2,US8563698B2',
            displaySearch: true,
            result: {}
        });
    }

    changePatents = (event) => {
        this.setState({
            patentIds: event.target.value
        });
    }

    handleSubmit = () => {
        const url = '/upload'
        
        fetch(url, {
            method: 'POST',
            body: JSON.stringify(this.state)
        })
        .then(response => response.json())
        .then(result => {
            console.log(result);
            this.setState({
                displaySearch: false,
                result: result.message
            })
        });
    }

    handleBack = () => {
        ReactDOM.unmountComponentAtNode(document.getElementById('my-msa'));
        this.resetState();
    }

    setViewerOptions = () => {
        const sequences = []
        const epitopes = []
        for (const name in this.state.result) {
            const sequence = {
                name: name,
                sequence: this.state.result[name]["sequences"]
            };
            sequences.push(sequence);
            epitopes.push(this.state.result[name]["epitopes"])
        }

        const myColorScheme = new MyColorScheme(epitopes);
        var options = {
            colorScheme: myColorScheme,
            sequences: sequences
        }

        ReactDOM.render(
            React.createElement(ReactMSAViewer.MSAViewer, options),
            document.getElementById('my-msa')
        );
    }

    render() {
        if (this.state.displaySearch) {
            document.querySelector("#msa-container").style.display = "none";
            return (
                <div>
                    <div className="card mx-auto" style={{width: "40rem", margin: "5rem"}}>
                        <div className="card-body">
                            <div className="form-group">
                                <label htmlFor="txtPatents">Patent Ids:</label>
                                <input type="text" className="form-control" id="txtPatents"  value={this.state.patentIds} onChange={this.changePatents}></input>
                            </div>
                            <div>
                                <button className="btn btn-primary" onClick={this.handleSubmit}>
                                    Submit
                                </button>  
                            </div>      
                        </div>  
                    </div>       
                </div>
            )
        }        
        document.querySelector("#msa-container").style.display = "block";
        this.setViewerOptions();
        return (
            <button className="btn btn-primary" onClick={this.handleBack}>
                Back
            </button> 
        );
    }
}

class App extends React.Component {


    render() {
        return (
            <FileUpload />
        )
    }
}

ReactDOM.render(<App />, document.querySelector("#app"));