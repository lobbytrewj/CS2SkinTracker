import React, { useEffect, useState } from 'react';
import { Grid, Card, CardContent, Typography, CircularProgress } from '@mui/material';
import { api } from '../../services/api';

interface Item {
  item_id: string;
  market_hash_name: string;
  type: string;
  buff_price?: number;
  steam_price?: number;
}

const ItemList: React.FC = () => {
  const [items, setItems] = useState<Item[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchItems = async () => {
      try {
        const response = await api.getItems();
        setItems(response.data);
      } catch (error) {
        console.error('Error fetching items:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchItems();
  }, []);

  if (loading) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', padding: '2rem' }}>
        <CircularProgress />
      </div>
    );
  }

  return (
    <Grid container spacing={3}>
      {items.map((item) => (
        <Grid item xs={12} sm={6} md={4} key={item.item_id}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                {item.market_hash_name}
              </Typography>
              <Typography color="textSecondary">
                Type: {item.type}
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
            </CardContent>
          </Card>
        </Grid>
      ))}
    </Grid>
  );
};

export default ItemList;