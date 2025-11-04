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
  Grid,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  FormControlLabel,
  Checkbox
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import apiClient from '../utils/api';

function LeadScorer() {
  const navigate = useNavigate();
  const [leadData, setLeadData] = useState({
    company_size: 0,
    industry: '',
    budget: 0,
    engagement_level: 'low',
    is_decision_maker: false
  });
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleScore = async () => {
    // Validate required fields
    if (leadData.company_size < 0) {
      setError('Company size cannot be negative');
      return;
    }

    if (leadData.budget < 0) {
      setError('Budget cannot be negative');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await apiClient.post('/tasks/lead-score', {
        task_type: 'lead_score',
        parameters: {
          lead_data: leadData
        }
      });

      setResult(response.data.result);
    } catch (err) {
      setError('Failed to score lead: ' + (err.response?.data?.detail || err.message));
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="md" sx={{ mt: 4 }}>
      <Button onClick={() => navigate('/')} sx={{ mb: 2 }}>
        ← Back to Dashboard
      </Button>

      <Paper sx={{ p: 3 }}>
        <Typography variant="h4" gutterBottom>
          Lead Scorer
        </Typography>

        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              label="Company Size (employees)"
              type="number"
              inputProps={{ min: 0 }}
              placeholder="Number of employees"
              value={leadData.company_size}
              onChange={(e) => setLeadData({...leadData, company_size: Math.max(0, parseInt(e.target.value) || 0)})}
            />
          </Grid>
          <Grid item xs={12} md={6}>
            <FormControl fullWidth>
              <InputLabel>Industry</InputLabel>
              <Select
                value={leadData.industry}
                onChange={(e) => setLeadData({...leadData, industry: e.target.value})}
              >
                <MenuItem value="technology">Technology</MenuItem>
                <MenuItem value="finance">Finance</MenuItem>
                <MenuItem value="healthcare">Healthcare</MenuItem>
                <MenuItem value="retail">Retail</MenuItem>
                <MenuItem value="manufacturing">Manufacturing</MenuItem>
                <MenuItem value="other">Other</MenuItem>
              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              label="Project Budget ($)"
              type="number"
              inputProps={{ min: 0, step: 1000 }}
              placeholder="Available budget in USD"
              value={leadData.budget}
              onChange={(e) => setLeadData({...leadData, budget: Math.max(0, parseFloat(e.target.value) || 0)})}
            />
          </Grid>
          <Grid item xs={12} md={6}>
            <FormControl fullWidth>
              <InputLabel>Engagement Level</InputLabel>
              <Select
                value={leadData.engagement_level}
                onChange={(e) => setLeadData({...leadData, engagement_level: e.target.value})}
              >
                <MenuItem value="low">Low</MenuItem>
                <MenuItem value="medium">Medium</MenuItem>
                <MenuItem value="high">High</MenuItem>
              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={12}>
            <FormControlLabel
              control={
                <Checkbox
                  checked={leadData.is_decision_maker}
                  onChange={(e) => setLeadData({...leadData, is_decision_maker: e.target.checked})}
                />
              }
              label="Is Decision Maker"
            />
          </Grid>
        </Grid>

        <Button
          variant="contained"
          onClick={handleScore}
          disabled={loading}
          sx={{ mt: 3, mb: 3 }}
        >
          {loading ? <CircularProgress size={24} /> : 'Score Lead'}
        </Button>

        {error && (
          <Alert severity="error" sx={{ mb: 3 }}>
            {error}
          </Alert>
        )}

        {result && (
          <Box>
            <Typography variant="h6" gutterBottom>
              Lead Score Results:
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

export default LeadScorer;