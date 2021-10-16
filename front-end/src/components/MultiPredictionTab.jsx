import React from 'react';
// custom components
import { SubmitButton, numberFormatter } from './InputControls.jsx';
// mui
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Typography from '@mui/material/Typography';
import Stack from '@mui/material/Stack';
import Divider from '@mui/material/Divider';


export default class MultiPredictionTab extends React.Component {

    render() {
        console.log('job data', this.props.jobData)
        console.log('pred values', this.props.preds)
        return (
            <>
                <Stack direction='row' justifyContent='space-between' sx={{ mr: '5px' }}>
                    <Typography sx={{ my: '5px' }}>
                        Click 'Submit' to view salaries.
                    </Typography>
                    <SubmitButton submitFunction={this.props.multiSubmitFunction} />
                </Stack>
                <Divider sx={{mt: '8px'}} />

                <TableContainer>
                    <Table>
                        <TableHead>
                            <TableRow>
                                <TableCell>Job Type</TableCell>
                                <TableCell align='right'>Degree</TableCell>
                                <TableCell align='right'>Major</TableCell>
                                <TableCell align='right'>Industry</TableCell>
                                <TableCell align='right'>Years of Experience</TableCell>
                                <TableCell align='right'>Miles from Metropolis</TableCell>
                                <TableCell align='right'>Salary</TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {this.props.jobData.map((job) => {
                                let salaryText = this.props.preds[job.id] ? numberFormatter.format(this.props.preds[job.id] * 1000) : '---'

                                return (
                                    <TableRow key={job.id}>
                                        <TableCell>{job.jobType.replace('_', ' ')}</TableCell>
                                        <TableCell align='right'>{job.degree.replace('_', ' ')}</TableCell>
                                        <TableCell align='right'>{job.major}</TableCell>
                                        <TableCell align='right'>{job.industry}</TableCell>
                                        <TableCell align='right'>{job.yearsExperience}</TableCell>
                                        <TableCell align='right'>{job.milesFromMetropolis}</TableCell>
                                        <TableCell align='right'>{salaryText}</TableCell>
                                    </TableRow>
                                )

                            })}
                        </TableBody>
                    </Table>
                </TableContainer>

            </>
        );
    };
;}