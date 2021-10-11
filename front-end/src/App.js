import React from 'react';
// Custom components
import { DropdownSelect, SliderInput } from './components/InputControls';
import { SinglePredictionOutput } from './components/SinglePredictionOutput';
// mui
import Stack from '@mui/material/Stack';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import AppBar from '@mui/material/AppBar';
import Paper from '@mui/material/Paper';
import Divider from '@mui/material/Divider';
// css
import css from './css/main-styles.module.css';
// programatically generated dropdown menus
import dropdownMenuData from './data/dropdownSelectItems.json';



class App extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            jobTypeSelected: '',
            degreeSelected: '',
            majorSelected: '',
            industrySelected: '',
            yearsExperienceSelected: 0,
            milesFromMetropolisSelected: 0,
            singlePrediction: []

        };
    };
    handleChange = (selected, varname) => {

        this.setState({ [varname]: selected });

    }

    submit = () => {

        const predictionInput = {
            'jobType': this.state.jobTypeSelected,
            'degree': this.state.degreeSelected,
            'major': this.state.majorSelected,
            'industry': this.state.industrySelected,
            'yearsExperience': this.state.yearsExperienceSelected,
            'milesFromMetropolis': this.state.milesFromMetropolisSelected
        };

        let requestOptions = {
            method: "POST",
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(predictionInput)
        };
        fetch('/submit-predictions', requestOptions)
            .then(response => response.json())
            .then(data => this.setState({ singlePrediction: data.message }))

    };


    render() {
        let dropdown_menus = dropdownMenuData.map(menu =>
            <DropdownSelect
                selected={this.state[menu.stateName]}
                handleChange={this.handleChange}
                stateName={menu.stateName}
                label={menu.label}
                inputLabelId={menu.inputLabelId}
                menu_items={menu.menu_items}
                key={menu.stateName}

            />
        )

        return (

            <div id={css['bg-container']}>
                <AppBar position='static' sx={{ minHeight: 64 }}>
                    <Typography variant='h4' sx={{my: 'auto'}}>Salary Prediction</Typography>
                </AppBar>

                <Container maxWidth='lg' sx={{ mt: { lg: 7, md: 3, xs: 1 } }}>
                    <Paper elevation={10} sx={{ p: 1 }}>

                        <Typography>
                            Enter the job details below and click 'Submit' to get a predicted salary.
                        </Typography>
                        <br />

                        <div id="prediction-inputs">
                            <Divider textAlign='left'>
                                <Typography>
                                    Job Details
                                </Typography>
                            </Divider>
                            <Stack spacing={{ xs: 1, md: 4 }} sx={{ py: '20px' }}>
                                {/* Categorical drop down menu stack */}
                                <Stack direction={{ xs: 'column', sm: 'row' }} spacing={1} display='flex' justifyContent='space-around'>
                                    {dropdown_menus}
                                </Stack>

                                {/* Numeric slider input stack */}
                                <Stack
                                    direction={{ xs: 'column', sm: 'row' }}
                                    spacing={1} display='flex'
                                    justifyContent='space-around'
                                    alignItems='center'>

                                    <SliderInput
                                        label='Years of Experience'
                                        stateName='yearsExperienceSelected'
                                        selected={this.state['yearsExperienceSelected']}
                                        handleChange={this.handleChange}
                                        marks={[{ value: 0, label: '0' }, { value: 24, label: '24+' }]}
                                        min={0}
                                        max={24}
                                    />

                                    <SliderInput
                                        label='Miles from Metropolis'
                                        selected={this.state['milesFromMetropolisSelected']}
                                        handleChange={this.handleChange}
                                        stateName='milesFromMetropolisSelected'
                                        marks={[{ value: 0, label: '0' }, { value: 99, label: '99+' }]}
                                        min={0}
                                        max={99}
                                    />
                                </Stack>
                            </Stack>
                            <Typography className={css['required-caption']} variant='caption' color='grey' textAlign='right'>* Required</Typography>
                            <Divider />
                        </div>

                        <SinglePredictionOutput
                            submitFunction={this.submit}
                            prediction={this.state.singlePrediction}
                        />

                    </Paper>

                </Container>

            </div>

        );
    };

};

export default App;