import React from 'react';
import Stack from '@mui/material/Stack';
import Button from '@mui/material/Button';
import CheckIcon from '@mui/icons-material/Check';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';

import css from '../css/main-styles.module.css';


const numberFormatter = Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    maximumFractionDigits: 0
});

const NothingSubmitted = (props) => {
    return (
        <Typography className={css['nothing-predicted']}>-- Nothing submitted yet --</Typography>
    );
};

const PredictionText = (props) => {
    return (
        <Typography variant = 'h5'>{props.text}</Typography>
    );
};

export class SinglePredictionOutput extends React.Component {

    render() {
        let havePrediction = this.props.prediction.length == 1;
        let prediction_text;

        if (havePrediction) {
            prediction_text = numberFormatter.format(this.props.prediction[0] * 1000)
        };

        let outputDisplay = havePrediction ? <PredictionText text={prediction_text} /> : <NothingSubmitted />;

        return (
            <Stack id={css['prediction-output-container']} spacing={3}>
                {/* Submit button */}
                <Button
                    variant='contained'
                    color='success'
                    startIcon={<CheckIcon />}
                    onClick={() => this.props.submitFunction()}
                    sx={{ width: '320px' }}>
                    Submit
                </Button>

                {/* Prediction output */}
                <Box sx={{ border: '1px', borderStyle: 'dashed' }}>
                    <Stack spacing={2} sx={{ display: 'flex', alignItems: 'center', py: '15px', width: '320px' }}>
                        <Typography variant='h6'>
                            Predicted Salary:
                        </Typography>
                        {outputDisplay}

                    </Stack>
                </Box>
            </Stack>

        );
    };
};