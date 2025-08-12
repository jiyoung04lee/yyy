// partysmall 목록 
// import AppFrame from './components/AppFrame.jsx';
// import PartySmall from './partysmall_com/PartySamll.jsx';

// export default function App() {
//   return (
//     <AppFrame>
//       <div style={{ padding: 16 }}>
//         <PartySmall />
//       </div>
//     </AppFrame>
//   );
// }


// scrollpage.jsx
import AppFrame from './components/AppFrame.jsx';
import PhoneSheet from './scrollPage/PhoneSheet.jsx';
import './scrollPage/PhoneSheet.css';

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

