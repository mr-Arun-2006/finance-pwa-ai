import express, { Router, Request, Response } from 'express';

const router: Router = express.Router();

// Get forecast
router.get('/', (req: Request, res: Response) => {
  res.json({ message: 'Get forecast endpoint' });
});

// Generate forecast
router.post('/generate', (req: Request, res: Response) => {
  res.json({ message: 'Generate forecast endpoint' });
});

// Get forecast by category
router.get('/category/:categoryId', (req: Request, res: Response) => {
  res.json({ message: 'Get category forecast endpoint' });
});

// Get anomalies
router.get('/anomalies/detect', (req: Request, res: Response) => {
  res.json({ message: 'Detect anomalies endpoint' });
});

export default router;
