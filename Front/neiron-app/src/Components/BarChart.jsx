import React from 'react';
import { Bar } from 'react-chartjs-2';

const BarChart = () => {
    return (
        <Bar
            height={100}
            width={200}
            data={{labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange']}}/>

    );
};

export default BarChart;