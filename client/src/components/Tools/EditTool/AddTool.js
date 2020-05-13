import React from 'react';
import ReactModal from 'react-modal';
import './AddTool.css';

const initialState = {
    showAddToolModal: false,
    roNumber: 0,
    scancurrent: false,
    error: false,
    prescan: false,
    postscan: false,
    paired: false,
    errorID: 0,

};

class AddTool extends React.Component {

   state = initialState;

    handleAddToolModal = () => {
        this.setState({ showAddToolModal: !this.state.showAddToolModal});
    }



    handleSubmit = e => {
        e.preventDefault();
        const newTool = {...this.state}
        delete newTool.showAddToolModal;
        this.props.createTool(newTool)
        this.handleAddToolModal();
        this.setState(initialState);
    }

    render() {
        return (
            <div>
                <div className="button-menu">
                <button onClick={this.handleAddToolModal} 
                        className="add-tool-button">
                    Add Tool 
                </button>
                <div className="buttonBorder" id="border"></div>
                </div>

                <ReactModal isOpen={this.state.showAddToolModal}
                            contentLabel="Add Tools Modal"
                            style={addToolsStyle}
                            >

                            <form onSubmit={this.handleSubmit} 
                                  className="input-form">

                                <div className="add-tool-form">

                                    <div className="card-add-tool"> 

                                        <textarea type="text"
                                                name="toolNumber"
                                                key={this.toolName}
                                                className="card-text-inputs"
                                                placeholder="*Tool Name*"
                                                onChange={(e) => this.setState({toolName: e.target.value})}/>
                                    </div>
                                </div>

                                <div className="card-buttons">

                                    <h5 className="card-warning">*Tool Name*</h5>

                                        <button onClick={this.handleAddToolModal} 
                                                className="add-tool-menu-button cancel-button">
                                            Cancel
                                        </button>

                                        <button className="add-tool-menu-button submit-button">
                                            Submit
                                        </button>
                                </div>
                            </form>
                </ReactModal>
            </div>
        )
    }
} 
const addToolsStyle = {
    overlay: {
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        backgroundColor: 'rgba(216, 217, 222, 0.75)'
      },
      content: {
        position: 'fixed',
        top: '25%',
        left: '15%',
        right: '50%',
        bottom: '50%',
      
        width: '275px',
        marginTop: '10px',
        height: '120px',
        border: '2px solid #6e7889',
        background: '#f9f9f9',
        overflow: 'hidden',
        WebkitOverflowScrolling: 'touch',
        borderRadius: '4px',
        outline: 'none',
        padding: 0,
      }
}

export default AddTool