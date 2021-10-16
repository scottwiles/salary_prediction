import React from 'react';
// Custom components
import InputsTab from './components/InputsTab';
import MultiPredictionTab from './components/MultiPredictionTab';
// mui
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import AppBar from '@mui/material/AppBar';
import Paper from '@mui/material/Paper';
import Tab from '@mui/material/Tab';
import TabPanel from '@mui/lab/TabPanel';
import TabContext from '@mui/lab/TabContext';
import TabList from '@mui/lab/TabList'
import Toolbar from '@mui/material/Toolbar';
import IconButton from '@mui/material/IconButton';
import MenuIcon from '@mui/icons-material/Menu';
import Menu from '@mui/material/Menu';
import MenuItem from '@mui/material/MenuItem';
import Divider from '@mui/material/Divider';
import GitHubIcon from '@mui/icons-material/GitHub';
import LinkedInIcon from '@mui/icons-material/LinkedIn';
// css
import css from './css/main-styles.module.css';

const github_link = 'https://github.com/scottwiles/salary_prediction';
const linkedin_link = 'https://www.linkedin.com/in/wiles-scott/';


// This level of the app will only manage the state of items that need to be known across tabs
// i.e. which tab is selected, whether or not multi predict is selected, the inputs for multi select
class App extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            tabValue: 'single',
            menuOpen: false,
            multiPredict: false,
            multiJobArray: [],
            // multiPredictValues is an object where keys are jobId's from the multiJobArray, and values are predicted salaries
            multiPredictValues: {} 
        };
    };

    changeTab = (event, newValue) => {
        this.setState({ tabValue: newValue })

    };

    toggleMenu = () => {
        let currentValue = this.state.menuOpen;
        this.setState({menuOpen: !currentValue});
    }

    handleMenuLink = (link) => {
        window.open(link, '_blank');
        this.toggleMenu();
    }

    handleMultiSwitch = () => {
        let multiEnabled = this.state.multiPredict;

        this.setState({multiPredict: !multiEnabled});
    };

    gotoMultiTab = () => {
        this.setState({tabValue: 'multi'})
    };

    // Add a job to the array during multi predict mode.
    // We use the array .concat() method because it returns a new array and doesn't mutate the state
    // 'job' param is an object containing job details
    addJobToList = (job) => {
        // create a new id based on length of currently added jobs
        let newId = this.state.multiJobArray.length;
        job.id = newId;
        // add job to the list
        let newJobList = this.state.multiJobArray.concat(job);

        // copy the predicted values and add an id key-value pair for the new job
        let predCopy = Object.assign({}, this.state.multiPredictValues);
        predCopy[newId] = '';

        // update the state, adding the new job to the list and to the predicted values object
        this.setState({multiJobArray: newJobList, multiPredictValues: predCopy});

    };

    submitMultiPredictions = () => {
        // Setup POST request
        let requestOptions = {
            method: "POST",
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(this.state.multiJobArray)
        };
        // API call
        fetch('/multiple-prediction', requestOptions)
            .then(response => response.json())
            .then(data => this.setState({multiPredictValues: data.message}))
    };

    render() {
        let menuAnchor = document.getElementById('menu-button');

        let numJobs = this.state.multiJobArray.length;
        console.log(this.state.multiJobArray);

        return (

            <div id={css['bg-container']}>
                <AppBar position='static' sx={{ minHeight: 64, flexFlow: 'row', justifyContent: 'space-between' }}>
                    <Typography variant='h4' sx={{ my: 'auto', ml: '15px' }}>Salary Prediction</Typography>

                    <Toolbar>
                        <IconButton
                            onClick={() => this.toggleMenu()}
                            id='menu-button'
                            size='large'
                            sx={{color: 'whitesmoke'}}
                        >
                            <MenuIcon/>
                        </IconButton>
                    </Toolbar>

                    <Menu open={this.state.menuOpen} onClose={this.toggleMenu} anchorEl={menuAnchor}>
                        <MenuItem onClick={() => this.handleMenuLink(github_link)}>
                            <GitHubIcon sx={{mr: '10px'}} />
                            View on GitHub
                        </MenuItem>
                        <Divider />
                        <MenuItem onClick={() => this.handleMenuLink(linkedin_link)}>
                            <LinkedInIcon sx={{mr: '10px'}} />
                            Connect on LinkedIn
                        </MenuItem>
                    </Menu>

                </AppBar>

                <Container maxWidth='lg' sx={{ mt: { lg: 7, md: 3, xs: 1 } }}>

                    {/* Main App container with tablist and tabpanels */}
                    <Paper elevation={10} sx={{ p: 1 }}>
                        <TabContext value={this.state.tabValue}>
                            <TabList onChange={this.changeTab} scrollButtons='auto'>
                                <Tab label='Inputs' value='single' index={0} />
                                <Tab label='Multi predict' value='multi' index={1} disabled={!this.state.multiPredict} />
                            </TabList>
                            <TabPanel sx={{ p: '5px' }} value='single' index={0}>
                                <InputsTab
                                    multiEnabled={this.state.multiPredict}
                                    multiSwitch={this.handleMultiSwitch}
                                    navFunction={this.gotoMultiTab} 
                                    numJobs={numJobs}
                                    addJobFunction={this.addJobToList}
                                />
                            </TabPanel>
                            <TabPanel sx={{ p: '5px' }} value='multi' index={1}>
                                <MultiPredictionTab
                                    jobData={this.state.multiJobArray}
                                    preds={this.state.multiPredictValues} 
                                    multiSubmitFunction={this.submitMultiPredictions}
                                />
                            </TabPanel>
                        </TabContext>
                    </Paper>

                </Container>
            </div>

        );
    };

};

export default App;