import React, { useState, useEffect } from 'react';
import {
  Container,
  Grid,
  Card,
  CardContent,
  Typography,
  Button,
  AppBar,
  Toolbar,
  Box
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import EmailIcon from '@mui/icons-material/Email';
import ReceiptIcon from '@mui/icons-material/Receipt';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

function Dashboard() {
  const navigate = useNavigate();
  const [tasks, setTasks] = useState([]);

  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/tasks`);
      if (response.data && Array.isArray(response.data.tasks)) {
        setTasks(response.data.tasks);
      } else {
        console.warn('Invalid tasks data format:', response.data);
        setTasks([]);
      }
    } catch (error) {
      console.error('Error fetching tasks:', error);
      setTasks([]);
    }
  };

  const automationTools = [
    {
      title: 'Email Parser',
      description: 'Parse and extract key information from emails',
      icon: <EmailIcon fontSize="large" />,
      path: '/email-parser',
      color: '#1976d2'
    },
    {
      title: 'Invoice Generator',
      description: 'Generate professional invoices automatically',
      icon: <ReceiptIcon fontSize="large" />,
      path: '/invoice-generator',
      color: '#388e3c'
    },
    {
      title: 'Lead Scorer',
      description: 'Score and qualify leads automatically',
      icon: <TrendingUpIcon fontSize="large" />,
      path: '/lead-scorer',
      color: '#f57c00'
    }
  ];

  return (
    <>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Automation Dashboard
          </Typography>
        </Toolbar>
      </AppBar>

      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
        <Typography variant="h4" gutterBottom>
          Automation Tools
        </Typography>
        
        <Grid container spacing={3}>
          {automationTools.map((tool, index) => (
            <Grid item xs={12} md={4} key={index}>
              <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
                <CardContent sx={{ flexGrow: 1 }}>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                    <Box sx={{ color: tool.color, mr: 2 }}>
                      {tool.icon}
                    </Box>
                    <Typography variant="h6" component="h2">
                      {tool.title}
                    </Typography>
                  </Box>
                  <Typography variant="body2" color="text.secondary" paragraph>
                    {tool.description}
                  </Typography>
                  <Button
                    variant="contained"
                    fullWidth
                    onClick={() => navigate(tool.path)}
                    sx={{ backgroundColor: tool.color }}
                  >
                    Open Tool
                  </Button>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>

        <Typography variant="h5" sx={{ mt: 4, mb: 2 }}>
          Recent Tasks
        </Typography>
        
        <Grid container spacing={2}>
          {tasks && tasks.length > 0 ? (
            tasks.slice(0, 5).map((task, index) => (
              <Grid item xs={12} key={task.task_id || index}>
                <Card>
                  <CardContent>
                    <Typography variant="h6">{task.task_id || 'Unknown Task'}</Typography>
                    <Typography color="text.secondary">
                      Status: {task.status || 'Unknown'}
                    </Typography>
                    {task.timestamp && (
                      <Typography variant="caption" color="text.secondary">
                        {new Date(task.timestamp).toLocaleString()}
                      </Typography>
                    )}
                  </CardContent>
                </Card>
              </Grid>
            ))
          ) : (
            <Grid item xs={12}>
              <Card>
                <CardContent>
                  <Typography color="text.secondary">
                    No recent tasks found. Start using the automation tools above!
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          )}
        </Grid>
      </Container>
    </>
  );
}

export default Dashboard;