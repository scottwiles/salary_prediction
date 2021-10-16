import React from 'react';
// custom components
import { SubmitButton, numberFormatter } from './InputControls';
// mui
import Stack from '@mui/material/Stack';
import Button from '@mui/material/Button';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import NavigateNextOutlinedIcon from '@mui/icons-material/NavigateNextOutlined';
import AddOutlinedIcon from '@mui/icons-material/AddOutlined';
// styles
import css from '../css/main-styles.module.css';


const NothingSubmitted = () => {
    return (
        <Typography className={css['nothing-predicted']}>-- Nothing submitted yet --</Typography>
    );
};

const PredictionText = (props) => {
    return (
        <Typography variant='h5'>{props.text}</Typography>
    );
};

// Receives a function passed from the main app to add to the array of jobs
const AddButton = props => {

    return (
        <Box sx={{ width: '320px' }}>
            <Button
                variant='outlined'
                startIcon={<AddOutlinedIcon />}
                sx={{ width: '80%' }}
                onClick={() => props.addFunction()}
            >
                Add Job
            </Button>
            <Button
                variant='outlined'
                title="Go to 'Multi Predict' tab"
                onClick={() => props.navFunction()}
            >
                <NavigateNextOutlinedIcon />
            </Button>

        </Box>
    );
};

// The display text for single prediction mode
const SingleDisplay = (props) => {

    return (
        <Stack spacing={2} sx={{ display: 'flex', alignItems: 'center', py: '15px' }}>
            <Typography variant='h6'>
                Salary:
            </Typography>
            {props.text}
        </Stack>
    );
};

// The display text for multi predict mode
const MultiDisplay = (props) => {

    return (

        <Stack sx={{textAlign:'center', py: '10px', px: '5px'}}>
            <Typography variant='h6' sx={{mb: '10px'}}>
                Jobs added: {props.numJobs}
            </Typography>
            <Typography >
                View salaries on the 'Multi Predict' tab.
            </Typography>
        </Stack>

    );
};

export class SinglePredictionOutput extends React.Component {

    render() {
        let havePrediction = this.props.prediction.length === 1;
        let prediction_text;

        if (havePrediction) {
            prediction_text = numberFormatter.format(this.props.prediction[0] * 1000)
        };

        // Until there is a prediction submitted, show a 'nothing submitted' text
        let outputDisplay = havePrediction ? <PredictionText text={prediction_text} /> : <NothingSubmitted />;

        // If multi predict is enabled, show add job button to add each job to a list - otherwise show submit button
        let actionButton = this.props.multiEnabled ? <AddButton navFunction={this.props.navFunction} addFunction={this.props.addFunction} /> : <SubmitButton submitFunction={this.props.submitFunction} />;

        // If predicting single salary, show text with predicted value
        let outputTextBox = this.props.multiEnabled ? <MultiDisplay numJobs={this.props.numJobs} /> : <SingleDisplay text={outputDisplay} />;

        return (
            <Stack id={css['prediction-output-container']} spacing={3}>
                {/* Either the submit button or add button, depending on the multi predict switch value */}
                {actionButton}

                {/* Prediction output */}
                <Box sx={{ border: '1px', borderStyle: 'dashed', width: '320px'  }}>
                    {outputTextBox}
               </Box>
            </Stack>

        );
    };
};