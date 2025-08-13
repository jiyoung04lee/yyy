import { useEffect, useRef, useState } from 'react';
import './Scroll_Sheet.css';
import PartySmall from '../partysmall_com/PartySmall.jsx';
import PartySmallImages from '../images/partysmall.jpg';

export default function PhoneSheet() {
  // useRef - 리렌더 없이 값 기억 
  const sheetRef = useRef(null);          // 시트 DOM 참조 
  const startY = useRef(0);               // 드래그 시작  좌표
  const startPct = useRef(0);             // 드래그 시작 시트 높이(%) 
  const activePointerId = useRef(null);   // 추적하는 포인터 ID
  const stageHRef = useRef(1);            // 부모 높이(px) 캐시

  // 두 상태 스냅(최소/전체)
  const MIN_PCT = 30;                     // 최저 높이(%)
  const MAX_PCT = 100;                    // 최고 높이(%)
  const MID_THRESHOLD = (MIN_PCT + MAX_PCT) / 2; // 중앙 임계치(기본 65)
  const MID_BAND = 4;                     // 중앙 밴드(%): 전환 히스테리시스

  // 시트 높이 관리 (초기 최소)
  const [heightPct, setHeightPct] = useState(MIN_PCT);
  const isExpanded = heightPct >= 99.5;   /* 📍 이후 네비게이션 들어오면 조정 필요  */

  // 배경 스크롤 락 (100%일 때만)
  useEffect(() => {
    const prev = document.body.style.overflow;
    if (isExpanded) document.body.style.overflow = 'hidden';
    return () => { document.body.style.overflow = prev; };
  }, [isExpanded]);

  // 부모(.phone-stage) 높이 계산
  const getStageHeight = () => {
    const el = sheetRef.current;
    if (!el) return 1;
    const stage = el.parentElement;
    return Math.max(stage?.clientHeight ?? el.clientHeight, 1);
  };

  // 범위 고정 
  const clamp = (n, min = MIN_PCT, max = MAX_PCT) => Math.min(Math.max(n, min), max);

  // 드래그 값 저장 
  const beginDrag = (clientY) => {
    startY.current = clientY;
    startPct.current = heightPct;
    stageHRef.current = getStageHeight(); // ← 여기서 1회 측정
  };

  const moveDrag = (clientY) => {
    if (activePointerId.current == null) return;
    const dy = clientY - startY.current;
    const deltaPct = -(dy / stageHRef.current) * 100;
    const candidate = clamp(startPct.current + deltaPct);

    // 이진 스냅 미리 반영(중앙 밴드 벗어날 때만 전환)
    let target = heightPct; // 기본은 현재 상태 유지
    if (candidate >= MID_THRESHOLD + MID_BAND / 2) target = MAX_PCT;
    else if (candidate <= MID_THRESHOLD - MID_BAND / 2) target = MIN_PCT;

    setHeightPct(target);
  };

  const endDrag = () => {
    if (activePointerId.current == null) return;
    // 손을 떼면 두 상태 중 하나로 확정
    setHeightPct(heightPct >= MID_THRESHOLD ? MAX_PCT : MIN_PCT);
  };

  // 포인터 이벤트 핸들러 (마우스/터치 공통)
  const onPointer = (e) => {
    if (e.type === 'pointerdown') {
      const fromGrabber = e.target.closest('[data-grabber="true"]');
      if (isExpanded && !fromGrabber) return;

      activePointerId.current = e.pointerId;

      // 안전 체크 후 캡처
      const t = e.currentTarget;
      if (t && typeof t.setPointerCapture === 'function') {
        t.setPointerCapture(e.pointerId);
      }

      beginDrag(e.clientY);
    }

    if (e.type === 'pointermove') {
      if (activePointerId.current !== e.pointerId) return;
      moveDrag(e.clientY);
    }

    if (e.type === 'pointerup' || e.type === 'pointercancel') {
      if (activePointerId.current !== e.pointerId) return;

      const t = e.currentTarget;
      if (
        t &&
        typeof t.hasPointerCapture === 'function' &&
        typeof t.releasePointerCapture === 'function' &&
        t.hasPointerCapture(e.pointerId)
      ) {
        t.releasePointerCapture(e.pointerId);
      }

      activePointerId.current = null;
      endDrag();
    }
  };

  // 휠로 높이 제어 : 즉시 MIN/MAX 전환 (데스크톱 전용)
  const onWheel = (e) => {
    if (isExpanded) return;            // 펼쳐졌으면 내부 스크롤에 양보
    e.preventDefault();
    const goingUp = e.deltaY < 0;      // 위로 → 전체, 아래로 → 최소
    setHeightPct(goingUp ? MAX_PCT : MIN_PCT);
  };

  //Partysmall 컴포넌트 넣기 
  const parties = [
    {
      id: 'p1',
      eventTitle: '#유학생과_언어교류',
      eventDate: '2025-08-25T18:00:00',
      placeName: '주당끼리',
      attendees: 12,
      capacity: 20,
      placeImageUrl: PartySmallImages, 
    },
    // ...더 많은 파티
  ];

  return (
    <div
      ref={sheetRef}
      className="bottom-sheet"
      style={{
        height: `${heightPct}%`,
        // 펼쳐졌을 땐 내부 스크롤을 위해 터치 제스처를 브라우저에 위임
        // (접혀있을 땐 우리가 드래그 제스처를 처리)
        touchAction: isExpanded ? 'auto' : 'none',
      }}
      onPointerDown={onPointer}
      onPointerMove={onPointer}
      onPointerUp={onPointer}
      onPointerCancel={onPointer}
      onWheel={onWheel}
    >
      {/* grabber에서 시작하면 언제나 드래그 가능 */}
      <div className="grabber" data-grabber="true" />

      <div
        className="sheet-scroll"
        // 접혀있을 땐 시트만 드래그해야 하므로 내부 상호작용 차단
        style={{ pointerEvents: isExpanded ? 'auto' : 'none' }}
      >
        {/* ▶ 여기부터 목록 */}
        <ul className="party-list">
          {parties.map(p => (
            <li key={p.id}>
              <PartySmall
                {...p}
                onClick={() => console.log('상세보기:', p.id)}
              />
            </li>
          ))}
        </ul>
        {/* ◀ 여기까지 */}
      </div>
    </div>
  );
}

