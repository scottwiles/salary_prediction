import React from 'react';
// custom components
import { DropdownSelect, SliderInput, MultiPredictSwitch } from './InputControls';
import { SinglePredictionOutput } from './SinglePredictionOutput';
// mui
import Stack from '@mui/material/Stack';
import Typography from '@mui/material/Typography';
import Divider from '@mui/material/Divider';
import Snackbar from '@mui/material/Snackbar';
import Alert from '@mui/material/Alert';
// programatically generated dropdown menus
import dropdownMenuData from '../data/dropdownSelectItems.json';
// css
import css from '../css/main-styles.module.css';


// This component's state needs to manage only things that are related to single prediction,
// It should also be passed a function from the parent component to add entries to multi predict.
export default class InputsTab extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            jobTypeSelected: '',
            degreeSelected: '',
            majorSelected: '',
            industrySelected: '',
            yearsExperienceSelected: 0,
            milesFromMetropolisSelected: 0,
            singlePredictionValue: [],
            invalidInputAlert: false,
            missingInputs: []
        };
    };
    // General purpose function to handle input change from all input controls
    handleInputChange = (selected, varname) => {

        this.setState({ [varname]: selected });

    };

    // Get the inputs into an object that has variable names compatible with the prediction model
    collectJobDetails = () => {
        const jobDetail = {
            'jobType': this.state.jobTypeSelected,
            'degree': this.state.degreeSelected,
            'major': this.state.majorSelected,
            'industry': this.state.industrySelected,
            'yearsExperience': this.state.yearsExperienceSelected,
            'milesFromMetropolis': this.state.milesFromMetropolisSelected
        };

        return jobDetail;
    };

    resetInputs = () => {
        this.setState({
            jobTypeSelected: '',
            majorSelected: '',
            degreeSelected: '',
            industrySelected: '',
            yearsExperienceSelected: 0,
            milesFromMetropolisSelected: 0
        })
    };

    validateInputs = (inputs) => {

        let missingInputs = [];

        let friendlyNameMapping = {
            'jobType': 'Job Type',
            'degree': 'Degree',
            'industry': 'Industry',
            'major': 'Major'
        };

        // Iterate over the given inputs and add any missing inputs to the missingInputs array
        Object.entries(inputs).forEach(([key, value]) => {
            if (value === '') {
                missingInputs.push(friendlyNameMapping[key]);
            }
        });

        if (missingInputs.length > 0) {
            this.setState({invalidInputAlert: true, missingInputs: missingInputs})
            return false
        } else {
            return true
        }

    };

    // Submit currently selected options for prediction
    submitSinglePrediction = () => {
        // object to be JSON.stringify'd 
        const predictionInput = this.collectJobDetails();

        if (!this.validateInputs(predictionInput)) {
            return
        };

        // Setup a POST request
        let requestOptions = {
            method: "POST",
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(predictionInput)
        };
        // API request
        fetch('/single-prediction', requestOptions)
            .then(response => response.json())
            .then(data => this.setState({ singlePredictionValue: data.message }))

    };

    addJobDetails = () => {
        const jobDetails = this.collectJobDetails();

        if (!this.validateInputs(jobDetails)) {
            return
        }
        // Use function from parent component to manage state
        this.props.addJobFunction(jobDetails);
        // Reset the inputs for the next job, to prevent accidental duplicates
        this.resetInputs();
    };

    closeAlert = () => {
        this.setState({invalidInputAlert: false})

    };

    render() {
        let dropdown_menus = dropdownMenuData.map(menu =>
            <DropdownSelect
                selected={this.state[menu.stateName]}
                handleChange={this.handleInputChange}
                stateName={menu.stateName}
                label={menu.label}
                inputLabelId={menu.inputLabelId}
                menu_items={menu.menu_items}
                key={menu.stateName}

            />
        );

        return (
            <>
                <Typography sx={{ my: '5px' }}>
                    Enter the job details below and click 'Submit' to get a predicted salary.
                </Typography>

                <div id="prediction-inputs">
                    <Divider textAlign='left'>
                        <Typography>
                            Job Details
                        </Typography>
                    </Divider>

                    <MultiPredictSwitch checked={this.props.multiEnabled} onClick={() => this.props.multiSwitch()} />

                    <Stack spacing={{ xs: 1, md: 4 }} sx={{ py: '20px' }}>

                        {/* Categorical drop down menu stack */}
                        <Stack direction={{ xs: 'column', sm: 'row' }} spacing={1} display='flex' justifyContent='space-around'>
                            {/* Categorical dropdown menus */}
                            {dropdown_menus}
                        </Stack>

                        {/* Numeric slider input stack */}
                        <Stack
                            direction={{ xs: 'column', sm: 'row' }}
                            spacing={1} display='flex'
                            justifyContent='space-around'
                            alignItems='center'>

                            {/* Years of experience slider input */}
                            <SliderInput
                                label='Years of Experience'
                                stateName='yearsExperienceSelected'
                                selected={this.state['yearsExperienceSelected']}
                                handleChange={this.handleInputChange}
                                marks={[{ value: 0, label: '0' }, { value: 24, label: '24+' }]}
                                min={0}
                                max={24}
                            />

                            {/* Miles from metropolis slider input */}
                            <SliderInput
                                label='Miles from Metropolis'
                                selected={this.state['milesFromMetropolisSelected']}
                                handleChange={this.handleInputChange}
                                stateName='milesFromMetropolisSelected'
                                marks={[{ value: 0, label: '0' }, { value: 99, label: '99+' }]}
                                min={0}
                                max={99}
                            />
                        </Stack>
                    </Stack>
                    <Typography className={css['required-caption']} variant='caption' color='grey' textAlign='right'>* Required</Typography>
                    <Divider />
                    <Snackbar
                        open={this.state.invalidInputAlert}
                        anchorOrigin={{horizontal: 'center', vertical: 'top'}}
                        autoHideDuration={6000}
                        onClose={this.closeAlert}
                    >
                        <Alert
                            severity='error'
                            variant='filled'
                            sx={{width: '100%'}}
                            onClose={this.closeAlert}
                        >
                            <strong>Missing required inputs: </strong> {this.state.missingInputs.join(', ')}
                        </Alert>
                    </Snackbar>
                </div>

                <SinglePredictionOutput
                    submitFunction={this.submitSinglePrediction}
                    prediction={this.state.singlePredictionValue}
                    multiEnabled={this.props.multiEnabled}
                    navFunction={this.props.navFunction}
                    numJobs={this.props.numJobs}
                    addFunction={this.addJobDetails}
                />
            </>
        )
    }
}