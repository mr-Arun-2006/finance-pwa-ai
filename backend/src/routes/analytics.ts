import express, { Router, Request, Response } from 'express';

const router: Router = express.Router();

// Get dashboard analytics
router.get('/dashboard', (req: Request, res: Response) => {
  res.json({ message: 'Get dashboard analytics' });
});

// Get spending trends
router.get('/trends', (req: Request, res: Response) => {
  res.json({ message: 'Get spending trends' });
});

// Get category breakdown
router.get('/categories', (req: Request, res: Response) => {
  res.json({ message: 'Get category breakdown' });
});

// Get monthly summary
router.get('/monthly', (req: Request, res: Response) => {
  res.json({ message: 'Get monthly summary' });
});

export default router;
