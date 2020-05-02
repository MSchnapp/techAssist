import React from 'react'
import Modal from 'react-modal'
import axios from 'axios'
import './App.css'
import './Dashboard.scss';
import SingleTool from '../../components/Tools/SingleTool/SingleTool'
import LeftMenu from '../../components/Left Menu/LeftMenu'
import DashboardSidebarNav from '../../components/DashboardSidebarNav/DashboardSidebarNav'
import AddTool from '../../components/Tools/EditTool/AddTool'

Modal.setAppElement('#root')

class App extends React.Component {
    state = {
      tools: [],
      intervalIsSet: false,
      idToDelete: null,
      objectToUpdate: null,
      currentPage: 1,
      toolsPerPage: 16,
      searchTools: ''
    };
     
  
    componentDidMount() {
        this.getDataFromDb();
        if (!this.state.intervalIsSet) {
           let interval = setInterval(this.getDataFromDb);
           this.setState({ intervalIsSet: interval });
        }
    }

    componentWillUnmount() {
        if (this.state.intervalIsSet) {
            clearInterval(this.state.intervalIsSet);
            this.setState({ intervalIsSet: null });
        }
    }
    
    getDataFromDb = () => {
        fetch('http://localhost:3001/api/getData')
        .then((tools) => tools.json())
        .then((res) => this.setState({ tools: res.tools }))
    };


    handlePreScan = (tool) => {
        const newTool = {...tool, prescan : !tool.prescan}
        axios.put('http://localhost:3001/api/updateScanType', {
            tool: newTool})
            .then(res => console.log(res), this.getDataFromDb())
            .catch(err => console.log(err));
        }

    handlePostScan = (tool) => {
        const newTool = {...tool, postscan : !tool.postscan}
        axios.put('http://localhost:3001/api/updateScanType', {
            tool: newTool})
            .then(res => console.log(res), this.getDataFromDb())
            .catch(err => console.log(err));
    }

    handleScanCurrent = (tool) => {
        const newTool = {...tool, scancurrent : !tool.scancurrent}
        axios.put('http://localhost:3001/api/updateScanCurrent', {
            tool: newTool})
            .then(res => console.log(res), this.getDataFromDb())
            .catch(err => console.log(err));
    }

    handleErrorCurrent = (tool) => {
        const newTool = {...tool, error : !tool.error}
        axios.put('http://localhost:3001/api/updateError', {
            tool: newTool})
            .then(res => console.log(res), this.getDataFromDb())
            .catch(err => console.log(err));
    }

    createTool = (tool) => {
        console.log(tool)
        axios.post('http://localhost:3001/api/createTool', tool)
          .then(res => console.log(res), this.getDataFromDb())
          this.getDataFromDb()
      };

    deleteTool = (_id) => {
      console.log("Deleted")
      axios.delete('http://localhost:3001/api/deleteTool', {params: {_id: _id }})
        .then(res => console.log(res), this.getDataFromDb())
      };

    toggleNavSlider = () => {
        this.setState({navSliderVisible: !this.state.navSliderVisible})
    }

    getToolSearch = (toolSearch) => {
      console.log(toolSearch)
      axios.get('http://localhost:3001/api/searchTools', {params: {toolSearch}})
        .then((res) => this.setState({ success: true, tools: res.data.results, currentPage: 1}))
        .catch(err => console.log(err))
        console.log(this.state.tools)
        
    };

    handleChange = (e) => {
        this.setState({searchTools: e.target.value}, () => {
            const {searchTools} = this.state;
            this.getToolSearch(searchTools)})
    }

    handlePageClick(event) {
        this.setState({currentPage: Number(event.target.id)})
      }
    
    
    render() {
        const {tools, currentPage, toolsPerPage } = this.state;
        
        const indexOfLastTool = currentPage * toolsPerPage;

        const indexofFirstTool = indexOfLastTool - toolsPerPage;

        const currentTools = tools.slice(indexofFirstTool, indexOfLastTool)

        const renderTools = currentTools.map((tool, index) => {
            return <SingleTool key={index}
                               tool={tool}
                               handlePreScan={this.handlePreScan}
                               handlePostScan={this.handlePostScan}
                               handleScanCurrent={this.handleScanCurrent}
                               handleErrorCurrent={this.handleErrorCurrent}
                               deleteTool={this.deleteTool} />
        });

        const pageNumbers = [];
        for(let i = 1; i <= Math.ceil(tools.length / toolsPerPage); i++){
          pageNumbers.push(i)
        }
  
        const renderPageNumbers = pageNumbers.map(number => {
          return (
            <button
              key={number}
              id={number}
              className="page-number-button"
              onClick={this.handlePageClick.bind(this)}>{number}</button>
          )})

        return (
            <div className="dashboard-container">

            <DashboardSidebarNav {...this.props} navSliderVisible={this.state.navSliderVisible} toggleNavSlider={this.toggleNavSlider}>
                <LeftMenu />
                <AddTool createTool={this.createTool}/>
            </DashboardSidebarNav>
  
            <div className="dashboard-content">
  
            {/* Added this */}
            {/* this can be created in its own component and just pass the getToolSearch component down just like LeftBar */}
              <div className="search-header">
                <div className="hamburger-container hide-desktop" onClick={this.toggleNavSlider}>
                  <div className="hamburger-line"></div>
                  <div className="hamburger-line"></div>
                  <div className="hamburger-line"></div>
                </div>
  
                <div className="search-icon"></div>
                <input type="text" value={this.state.searchTools} onChange={this.handleChange} placeholder="Search Tools"/>
  
              </div>
            {/* To this */}
  
              <div className="dashboard-main-tool-view" style={{display: 'flex', flexWrap: 'wrap'}}>
                {renderTools}
              </div>
            </div>
            <div className="page-button">
              {renderPageNumbers}
              </div>
          </div>
        )
    }

}

export default App;