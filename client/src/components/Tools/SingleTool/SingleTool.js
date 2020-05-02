import React from 'react';
import ReactModal from 'react-modal';
import './SingleTool.css';
import './ToolModal.css';

class SingleTool extends React.Component {

    constructor(props) {
    super(props);
        this.state = {
            showToolModal: false,
        };

        this.handleCloseToolModal = this.handleCloseToolModal.bind(this);
        this.handleOpenToolModal = this.handleOpenToolModal.bind(this);
    }

    handleCloseToolModal () {
        this.setState({ showToolModal: false });
    }

    handleOpenToolModal () {
        this.setState({ showToolModal: true });
    }

    handleDeleteTool = (e) => {
        e.preventDefault();
        this.props.deleteTool(this.props.tool._id)
        this.handleCloseToolModal()
    }

    preScanTag = () => {
        return {
            color: 'white',
            display: this.props.tool.prescan ? '' : 'none',
            background: this.props.tool.prescan ? 'red' : 'white'
        }
    }

    postScanTag = () => {
        return {
            color: 'white',
            display: this.props.tool.postscan ? '' : 'none',
            background: this.props.tool.postscan ? 'red' : 'white'
        }
    }

    scancurrentTag = () => {
        return {
            backgroundColor: this.props.tool.scancurrent ? 'red' : 'green',
        }
    }

    errorTag = () => {
        return {
            background: this.props.tool.error ? 'red' : 'green',
        }
    }
    errorTagModal = () => {
        return {
            color: 'white',
            display: this.props.tool.error ? '' : 'none',
            background: this.props.tool.error ? 'red' : 'green'
        }
    }

    pairedTag = () => {
        return {
            background: this.props.tool.paired ? 'green' : 'red',
        }
    }

    preScanClicked = () => {
        return {
            backgroundColor: this.props.tool.prescan ? 'orange' : ''
        } 
    }

    postScanClicked = () => {
        return {
            backgroundColor: this.props.tool.postscan ? 'red' : '',
        }
    }

    errorClicked = () => {
        return {
            backgroundColor: this.props.tool.error ? 'red' : '',
        }
    }

    scancurrentWording = () => {
        if(this.props.tool.scancurrent === true) {
            return "Scan is Progress"
        }
        else { 
            return "Available" 
        }
    }

    render() {
        const { _id, toolName, roNumber, scancurrent, prescan, postscan, error, paired } = this.props.tool;

    return (
        <>
        <div className="card">

            <div className="card-tool-number">

                <div className="tool-number">{toolName}</div>

                <div className="tool-scancurrent" style={this.scancurrentTag()}>{scancurrent ? "Scan in Progress" : "Available"}</div>
                
                <div className="card-option-container">
                    <div className="card-option" id="scantype" style={this.preScanTag()}>{prescan ? 'PreScan' : ''}</div>
                    <div className="card-option" id="scantype" style={this.postScanTag()}>{postscan ? 'PostScan' : ''}</div>
                    <div className="card-option" style={this.errorTag()}>{error ? 'Error Current' : 'No Error'}</div>
                    <div className="card-option" id="ronumber">{roNumber} <br/> RO</div>
                    <div className="card-option" style={this.pairedTag()}>{paired ? 'Paired': 'Not Paired'}</div>
                </div>

                <div className="card-open-modal-button" onClick={this.handleOpenToolModal}>View Tool</div>
            
            </div>

        </div>

        <ReactModal
            isOpen={this.state.showToolModal}
            contentLabel="Tool"
            style={toolModalStyle}>

            <div className="tool-modal-container">

                <h1 className="tool-number-modal">{toolName}</h1>
                <p className="tool-id-modal">{_id}</p>
            
                <button onClick={this.handleDeleteTool} 
                      className="header-button-modal">
                   X
                </button>

                <div className="tool-attribute-modal">

                    <h4 className="roNumber-modal">{roNumber} RO Number</h4>

                    <h4 style={this.preScanTag()} 
                        className="prescan-tag-modal">PreScan</h4>

                    <h4 style={this.pairedTag()} 
                        className="paired-tag-modal">{paired ? 'Paired' : 'Not Paired'}</h4>

                    <h4 style={this.postScanTag()} 
                        className="postscan-tag-modal">PostScan</h4>

                    <h4 style={this.errorTagModal()} 
                        className="error-tag-modal">{error ? 'ERROR' : ''}</h4>
                    
                    <h4 style={this.scancurrentTag()}
                        className="available-tag-modal">{scancurrent ? 'Not Available' : 'Available'}</h4>

                </div>

                <button onClick={() => this.props.handlePreScan(this.props.tool)}
                      className="missing-button-modal button-modal"
                      style={this.preScanClicked()}>
                      PreScan
                </button>

                <button onClick={() => this.props.handlePostScan(this.props.tool)} 
                      className="broken-button-modal button-modal" 
                      style={this.postScanClicked()}>
                      Completion Scan
                </button>

                <button onClick={() => this.props.handleErrorCurrent(this.props.tool)} 
                      className="delete-button-modal button-modal" 
                      style={this.errorClicked()}>
                      Clear Error
                </button>

                <button onClick={() => this.props.handleScanCurrent(this.props.tool)} 
                      className="checkOut-button-modal button-modal" 
                      style={this.scancurrentTag()}>
                      {this.scancurrentWording()}
                </button>

                <button className="cancel-button-modal button-modal" 
                      onClick={this.handleCloseToolModal}>
                      Close
              </button>

            </div>

        </ReactModal>
        </>
    )
    }

} ;

const toolModalStyle = {
    overlay: {
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        backgroundColor: 'rgba(255, 255, 255, 0.75)'
      },
      content: {
        position: 'fixed',
        top: '30%',
        left: '30%',
        right: '50%',
        bottom: '50%',
        minWidth: '550px',
        minHeight: '300px',
        border: '2px solid #000',
        background: '#fff',
        overflow: 'auto',
        WebkitOverflowScrolling: 'touch',
        borderRadius: '4px',
        outline: 'none',
        margin: 0,
        padding: 0,
      }
}

export default SingleTool;
