import React, { Component } from 'react';
// import { connect } from 'react-redux';
// import { toggleNavSlider } from '../redux/actions/misc';
import './DashboardSidebarNav.scss';

class DashboardSidebarNav extends Component {

    render() {
        const { navSliderVisible } = this.props;
        let visibility = navSliderVisible ? "show" : "hide";
        // let visibility = true ? "show" : "hide";

        return (
            <div className={`dashboard-nav-container dashboard-nav-container-${visibility}`}>

                <div className={`dashboard-nav-background fade-in-${visibility}`}>
                </div>

                <div className={`dashboard-nav-sliding-container dashboard-nav-${visibility}`}>

                    <div className={"dashboard-nav"}>
                        <div className={"hide-desktop close"} onClick={this.props.toggleNavSlider}>&times;</div>

                        {this.props.children}

                    </div>

                    <div className={"dashboard-nav-close"} onClick={this.props.toggleNavSlider}>

                    </div>


                </div>

            </div>
        )
    }
}

// const mapStateToProps = state => ({
//     navSliderVisible: state.misc.navSliderVisible
// })

// const mapDispatchToProps = dispatch => ({
//     toggleNavSlider: () => dispatch(toggleNavSlider())
// })

// export default connect(mapStateToProps, mapDispatchToProps)(DashboardSidebarNav);
export default DashboardSidebarNav;

