import React from 'react';
import { Typography } from '@mui/material';
import ItemList from 'frontend/src/components/items/ItemList';

const Home = () => {
  return (
    <div>
      <Typography variant="h4" gutterBottom>
        Welcome to CS2 Skin Tracker
      </Typography>
      <ItemList />
    </div>
  );
};

export default Home;