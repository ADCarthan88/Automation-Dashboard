import React, { useState } from 'react';
import {
  Container,
  Paper,
  TextField,
  Button,
  Typography,
  Box,
  Alert,
  CircularProgress,
  Grid
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

function InvoiceGenerator() {
  const navigate = useNavigate();
  const [clientInfo, setClientInfo] = useState({
    name: '',
    email: '',
    address: ''
  });
  const [items, setItems] = useState([
    { description: '', quantity: 1, price: 0 }
  ]);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleGenerate = async () => {
    if (!clientInfo.name.trim()) {
      setError('Please enter client name');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await axios.post(`${API_BASE_URL}/tasks/invoice-generate`, {
        task_type: 'invoice_generate',
        parameters: {
          client_info: clientInfo,
          items: items
        }
      });

      setResult(response.data.result);
    } catch (err) {
      setError('Failed to generate invoice: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const addItem = () => {
    setItems([...items, { description: '', quantity: 1, price: 0 }]);
  };

  const updateItem = (index, field, value) => {
    const newItems = [...items];
    newItems[index][field] = value;
    setItems(newItems);
  };

  return (
    <Container maxWidth="md" sx={{ mt: 4 }}>
      <Button onClick={() => navigate('/')} sx={{ mb: 2 }}>
        ← Back to Dashboard
      </Button>

      <Paper sx={{ p: 3 }}>
        <Typography variant="h4" gutterBottom>
          Invoice Generator
        </Typography>

        <Typography variant="h6" sx={{ mt: 3, mb: 2 }}>
          Client Information
        </Typography>
        <Grid container spacing={2}>
          <Grid item xs={12}>
            <TextField
              fullWidth
              label="Client Name"
              value={clientInfo.name}
              onChange={(e) => setClientInfo({...clientInfo, name: e.target.value})}
            />
          </Grid>
          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              label="Email"
              value={clientInfo.email}
              onChange={(e) => setClientInfo({...clientInfo, email: e.target.value})}
            />
          </Grid>
          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              label="Address"
              value={clientInfo.address}
              onChange={(e) => setClientInfo({...clientInfo, address: e.target.value})}
            />
          </Grid>
        </Grid>

        <Typography variant="h6" sx={{ mt: 3, mb: 2 }}>
          Items
        </Typography>
        {items.map((item, index) => (
          <Grid container spacing={2} key={index} sx={{ mb: 2 }}>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Description"
                value={item.description}
                onChange={(e) => updateItem(index, 'description', e.target.value)}
              />
            </Grid>
            <Grid item xs={6} md={3}>
              <TextField
                fullWidth
                label="Quantity"
                type="number"
                value={item.quantity}
                onChange={(e) => updateItem(index, 'quantity', parseInt(e.target.value))}
              />
            </Grid>
            <Grid item xs={6} md={3}>
              <TextField
                fullWidth
                label="Price"
                type="number"
                value={item.price}
                onChange={(e) => updateItem(index, 'price', parseFloat(e.target.value))}
              />
            </Grid>
          </Grid>
        ))}

        <Button onClick={addItem} sx={{ mb: 3 }}>
          Add Item
        </Button>

        <Box>
          <Button
            variant="contained"
            onClick={handleGenerate}
            disabled={loading}
            sx={{ mb: 3 }}
          >
            {loading ? <CircularProgress size={24} /> : 'Generate Invoice'}
          </Button>
        </Box>

        {error && (
          <Alert severity="error" sx={{ mb: 3 }}>
            {error}
          </Alert>
        )}

        {result && (
          <Box>
            <Typography variant="h6" gutterBottom>
              Generated Invoice:
            </Typography>
            <Paper sx={{ p: 2, backgroundColor: '#f5f5f5' }}>
              <pre>{JSON.stringify(result, null, 2)}</pre>
            </Paper>
          </Box>
        )}
      </Paper>
    </Container>
  );
}

export default InvoiceGenerator;