import { configureStore } from '@reduxjs/toolkit';

const store = configureStore({
  reducer: {
    // To be added: slices for transactions, budgets, forecasts, etc.
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;

export default store;
