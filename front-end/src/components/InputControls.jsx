import React from 'react';
import MenuItem from '@mui/material/MenuItem';
import Select from '@mui/material/Select';
import InputLabel from '@mui/material/InputLabel';
import FormControl from '@mui/material/FormControl';
import Slider from '@mui/material/Slider';
import Paper from '@mui/material/Paper';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Stack from '@mui/material/Stack';
import FormGroup from '@mui/material/FormGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import Switch from '@mui/material/Switch';
import CheckIcon from '@mui/icons-material/Check';
import Button from '@mui/material/Button';

import css from '../css/main-styles.module.css';

export const numberFormatter = Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    maximumFractionDigits: 0
});

export const SubmitButton = (props) => {

    return (
        <Button
            variant='contained'
            color='success'
            startIcon={<CheckIcon />}
            onClick={() => props.submitFunction()}
            sx={{ width: '320px' }}>
            Submit
        </Button>
    );
};



// DropdownSelect component
// props:
// stateName - name of the state key that holds selected option in state
// label - user facing label
// selected - value of the currently selected option
// handleChange - function passed from parent component to manage state
// inputLabelId - used in the InputLabel component
export class DropdownSelect extends React.Component {

    processInputChange = selectedOption => {
        this.props.handleChange(selectedOption.target.value, this.props.stateName);

    }

    render() {
        const selectedItem = this.props.selected;

        let menu_items = this.props.menu_items.map(
            item => <MenuItem value={item.value} key={item.value}>{item.label}</MenuItem>
        );

        return (
            <FormControl sx={{ minWidth: 180 }} required>
                <InputLabel id={this.props.inputLabelId}>{this.props.label}</InputLabel>
                <Select
                    labelId={this.props.inputLabelId}
                    value={selectedItem}
                    label={this.props.label}
                    onChange={this.processInputChange}
                >
                    <MenuItem value=''><em>--</em></MenuItem>
                    {menu_items}
                </Select>
            </FormControl>
        )
    }
};

// SliderInput component
// props:
// stateName - name of the key that holds selected option in state
// selected - value of the currently selected value
// handleChange - function passed from parent component to manage state
// marks - marks passed to the Slider component for labeling the slider
export class SliderInput extends React.Component {

    processInputChange = selectedOption => {
        this.props.handleChange(selectedOption.target.value, this.props.stateName)
    };

    render() {
        const sliderValue = this.props.selected;

        return (
            <Paper elevation={2} sx={{ width: 330 }}>

                <Box sx={{ my: '3px', mx: '15px', display: 'flex', justifyContent: 'space-between' }}>
                    <Stack>
                        <Typography>{this.props.label}</Typography>

                        <Slider
                            value={sliderValue}
                            sx={{ width: 250 }}
                            onChange={this.processInputChange}
                            marks={this.props.marks}
                            min={this.props.min}
                            max={this.props.max}
                            valueLabelDisplay='auto'
                        />
                    </Stack>
                    <Typography variant='h4' sx={{ alignSelf: 'center' }}>
                        {this.props.selected}
                    </Typography>
                </Box>

            </Paper>
        );
    };
};

// This component receives a prop for handling click events, and manages the state of whether
// multi predictions are enabled
export const MultiPredictSwitch = (props) => {
    let switchEl = <Switch checked={props.checked} onClick={() => props.onClick()} />;

    return (
        <FormGroup className={css['noselect']} sx={{alignContent: 'end', mr: '10px'}} >
            <FormControlLabel
                control={switchEl}
                label='Multi Predict'
                labelPlacement='start'
                sx={{width: 'max-content'}}
            />
        </FormGroup>
    );
}