// scrollpage.jsx
import AppFrame from './components/AppFrame.jsx';
import PhoneSheet from './scrollPage/Scroll_sheet.jsx';

export default function App() {
  return (
    <AppFrame>
      <div className="phone-stage">
        {/* 여기 배경(지도나 이미지) 넣어도 됨 */}
        <PhoneSheet />
      </div>
    </AppFrame>
  );
}
