import React from 'react';
import { Bar } from 'react-chartjs-2';
import {Chart as ChartJS} from 'chart.js/auto'

const BarChart = ({CharData}) => {
    return (
            <Bar
                data={CharData}
            />



    );
};

export default BarChart;