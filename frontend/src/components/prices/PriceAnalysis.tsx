import React from 'react';
import { Card, Table, Badge } from 'react-bootstrap';

interface PriceStats {
    source: string;
    average_price: number;
    min_price: number;
    max_price: number;
}

interface PriceAnalysisProps {
    analysis: PriceStats[];
    itemName: string;
}

export const PriceAnalysis: React.FC<PriceAnalysisProps> = ({ analysis, itemName }) => {
    const getArbitrageDifference = () => {
        const steamPrice = analysis.find(a => a.source === 'steam')?.average_price || 0;
        const buffPrice = analysis.find(a => a.source === 'buff')?.average_price || 0;
        return ((steamPrice - buffPrice) / buffPrice * 100).toFixed(2);
    };

    return (
        <Card className="price-analysis">
            <Card.Header>
                <h3>{itemName} Price Analysis</h3>
            </Card.Header>
            <Card.Body>
                <Table striped bordered hover>
                    <thead>
                        <tr>
                            <th>Source</th>
                            <th>Average Price</th>
                            <th>Min Price</th>
                            <th>Max Price</th>
                        </tr>
                    </thead>
                    <tbody>
                        {analysis.map(stat => (
                            <tr key={stat.source}>
                                <td>{stat.source}</td>
                                <td>${stat.average_price.toFixed(2)}</td>
                                <td>${stat.min_price.toFixed(2)}</td>
                                <td>${stat.max_price.toFixed(2)}</td>
                            </tr>
                        ))}
                    </tbody>
                </Table>
                <div className="mt-3">
                    <h4>Arbitrage Opportunity</h4>
                    <Badge bg={Number(getArbitrageDifference()) > 10 ? 'success' : 'warning'}>
                        {getArbitrageDifference()}% difference
                    </Badge>
                </div>
            </Card.Body>
        </Card>
    );
};