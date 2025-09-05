import React, { useEffect, useState } from 'react';
import { Grid, Card, CardContent, Typography, CircularProgress, Container } from '@mui/material';
import { Link } from 'react-router-dom';
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
      <Container sx={{ display: 'flex', justifyContent: 'center', padding: '2rem' }}>
        <CircularProgress />
      </Container>
    );
  }

  return (
    <Container>
      <Grid container spacing={3}>
        {items.map((item) => (
        <Grid container spacing={2}>
            item 
            key={item.item_id}
            xs={12}
            sm={6}
            md={4}
            <Link 
              to={`/item/${item.item_id}`}
              style={{ textDecoration: 'none', width: '100%' }}
            >
              <Card sx={{ height: '100%' }}>
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
            </Link>
          </Grid>
        ))}
      </Grid>
    </Container>
  );
};

export default ItemList;