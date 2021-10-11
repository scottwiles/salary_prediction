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
            item => <MenuItem value = {item.value} key = {item.value}>{item.label}</MenuItem>
            );
    
        return (
            <FormControl sx={{ minWidth: 180 }} required>
                <InputLabel id={this.props.inputLabelId}>{this.props.label}</InputLabel>
                <Select
                    labelId={this.props.inputLabelId}
                    value={selectedItem}
                    label = {this.props.label}
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

            <Paper elevation={2} sx={{width: 330}}>

                <Box sx={{my: '3px', mx: '15px', display:'flex', justifyContent: 'space-between'}}>

                <Stack>
                    <Typography>{this.props.label}</Typography>

                    <Slider
                    value = {sliderValue}
                    sx = {{width: 250}}
                    onChange = {this.processInputChange}
                    marks = {this.props.marks}
                    min = {this.props.min}
                    max = {this.props.max}
                    valueLabelDisplay = 'auto'

                    />
                </Stack>
                <Typography variant='h4' sx={{alignSelf: 'center'}}>
                    {this.props.selected}
                </Typography>
                </Box>

            </Paper>


        )

    }
};