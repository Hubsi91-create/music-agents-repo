import StoryboardPage from './pages/StoryboardPage';
import './styles/globals.css';

/**
 * Main App Component
 *
 * Entry point for the Music Agents Dashboard
 * Currently renders the Storyboard Studio page
 */
function App() {
  return (
    <div className="app">
      <StoryboardPage />
    </div>
  );
}

export default App;
