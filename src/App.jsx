import AppFrame from './components/AppFrame.jsx';
import PhoneSheet from './scrollPage/Scroll_sheet.jsx';
import Header from './components/Header.jsx';

export default function App() {
  return (
    <AppFrame>
      <div className="phone-stage">
        <Header/>
        <PhoneSheet />
      </div>
    </AppFrame>
  );
}