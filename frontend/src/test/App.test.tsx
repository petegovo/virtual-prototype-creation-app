import { render, screen } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import App from '../App'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: false,
    },
  },
})

const AppWrapper = () => (
  <QueryClientProvider client={queryClient}>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </QueryClientProvider>
)

describe('App', () => {
  it('renders without crashing', () => {
    render(<AppWrapper />)
    expect(document.body).toBeInTheDocument()
  })

  it('renders the main layout', () => {
    render(<AppWrapper />)
    // The app should render the layout component
    expect(document.querySelector('.min-h-screen')).toBeInTheDocument()
  })
})