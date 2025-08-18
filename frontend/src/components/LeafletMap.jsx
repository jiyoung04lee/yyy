import React, { useEffect, useRef } from 'react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

// 백엔드에서 제공하는 지도 이미지 경로
const mapImageUrl = 'http://127.0.0.1:8000/static/map.png';
// 지도 이미지 크기.
const imageWidth = 822; //1513
const imageHeight = 460; // 846

const LeafletMap = ({ minSheetHeight, headerHeight }) => {
  const mapRef = useRef(null);
  const mapInstance = useRef(null);

  useEffect(() => {
    // 지도가 여러 번 초기화되는 것을 방지
    if (mapInstance.current) return;

    // 지도를 담을 컨테이너가 필요
    if (mapRef.current) {
      // 이미지 경계를 정의. 좌표는 [y, x] 형식.
      const bounds = [[0, 0], [imageHeight, imageWidth]];

      mapInstance.current = L.map(mapRef.current, {
        crs: L.CRS.Simple,
        zoomControl: false, // 확대/축소 버튼 비활성화
        maxBounds: bounds, // 맵 이동을 이미지 경계로 제한
        maxBoundsViscosity: 1.0, // 경계 밖으로 드래그 방지
        attributionControl: false, // Leaflet 저작권 표시 제거
      });

      const map = mapInstance.current;

      // 이미지 오버레이를 생성하여 지도에 추가
      L.imageOverlay(mapImageUrl, bounds).addTo(map);

      // 지도 뷰를 이미지 경계에 딱 맞게 설정 (패딩 없이)
      map.fitBounds(bounds, { padding: [0, 0] });

      // 현재 줌 레벨을 최소 줌 레벨로 설정하여 더 이상 축소되지 않도록 함
      map.setMinZoom(map.getZoom());
    }

    // 컴포넌트가 언마운트될 때 맵 인스턴스를 파괴하는 정리 함수
    return () => {
      if (mapInstance.current) {
        mapInstance.current.remove();
        mapInstance.current = null;
      }
    };
  }, []);

  return <div ref={mapRef} style={{ position: 'absolute', top: `${headerHeight}px`, left: 0, right: 0, bottom: `${minSheetHeight}%` }} />;
};

export default LeafletMap;
