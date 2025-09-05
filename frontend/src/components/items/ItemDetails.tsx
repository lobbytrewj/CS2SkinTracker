import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { Container, Paper, Typography, Box, CircularProgress } from '@mui/material';
import { api } from '../../services/api';
import { PriceChart } from '../prices/PriceChart';

interface Item {
  item_id: string;
  market_hash_name: string;
  type: string;
  buff_price?: number;
  steam_price?: number;
}

interface PriceHistory {
  price: number;
  timestamp: string;
  source: string;
}

const ItemDetails: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [item, setItem] = useState<Item | null>(null);
  const [priceHistory, setPriceHistory] = useState<PriceHistory[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchItemDetails = async () => {
      try {
        if (!id) return;
        
        const [itemResponse, priceResponse] = await Promise.all([
          api.getItem(id),
          api.getPriceHistory(id)
        ]);

        setItem(itemResponse.data);
        setPriceHistory(priceResponse.data);
      } catch (error) {
        console.error('Error fetching item details:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchItemDetails();
  }, [id]);

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" p={4}>
        <CircularProgress />
      </Box>
    );
  }

  if (!item) {
    return (
      <Container>
        <Typography variant="h5" color="error">
          Item not found
        </Typography>
      </Container>
    );
  }

  return (
    <Container>
      <Paper sx={{ p: 3, mt: 3 }}>
        <Typography variant="h4" gutterBottom>
          {item.market_hash_name}
        </Typography>
        <Typography variant="subtitle1" gutterBottom>
          Type: {item.type}
        </Typography>
        
        <Box sx={{ mt: 2, mb: 2 }}>
          <Typography variant="h6" gutterBottom>
            Current Prices
          </Typography>
          {item.buff_price && (
            <Typography>
              Buff Price: ${item.buff_price.toFixed(2)}
            </Typography>
          )}
          {item.steam_price && (
            <Typography>
              Steam Price: ${item.steam_price.toFixed(2)}
            </Typography>
          )}
        </Box>

        <Box sx={{ mt: 4 }}>
          <PriceChart 
            data={priceHistory}
            itemName={item.market_hash_name}
          />
        </Box>
      </Paper>
    </Container>
  );
};

export default ItemDetails;