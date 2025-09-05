import React from 'react';
import { Card, CardContent, Typography } from '@mui/material';
import { Line } from 'react-chartjs-2';
import { 
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
} from 'chart.js';

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
);

interface PriceData {
    price: number;
    timestamp: string;
    source: string;
}

interface PriceChartProps {
    data: PriceData[];
    itemName: string;
}

export const PriceChart: React.FC<PriceChartProps> = ({ data, itemName }) => {
    const steamData = data.filter(d => d.source === 'steam');
    const buffData = data.filter(d => d.source === 'buff');

    const chartData = {
        labels: steamData.map(d => new Date(d.timestamp).toLocaleDateString()),
        datasets: [
            {
                label: 'Steam Price',
                data: steamData.map(d => d.price),
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1
            },
            {
                label: 'Buff Price',
                data: buffData.map(d => d.price),
                borderColor: 'rgb(255, 99, 132)',
                tension: 0.1
            }
        ]
    };

    return (
        <Card>
            <CardContent>
                <Typography variant="h6" gutterBottom>
                    {itemName} Price History
                </Typography>
                <Line data={chartData} />
            </CardContent>
        </Card>
    );
};