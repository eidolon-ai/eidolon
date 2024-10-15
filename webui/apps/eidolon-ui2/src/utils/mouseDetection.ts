import {useCallback, useEffect, useRef, useState} from 'react';

const useMouseLeaveDetection = (callback: () => void): void => {
  const handleMouseOut = useCallback((event: MouseEvent) => {
    if (!inWindow(event)) {
      callback();
    }
  }, [callback]);

  useEffect(() => {
    document.addEventListener('mouseout', handleMouseOut);

    return () => {
      document.removeEventListener('mouseout', handleMouseOut);
    };
  }, [handleMouseOut]);
};

export const inWindow = (event: MouseEvent): boolean => {
  return !(
    event.clientY <= 0 ||
    event.clientX <= 0 ||
    event.clientX >= window.innerWidth ||
    event.clientY >= window.innerHeight
  );
}

export interface UseMouseTrackingOptions {
  initialIsPinned?: boolean;
  onMouseEnter?: () => void;
  onMouseLeave?: () => void;
}

export function useMouseTracking({
  initialIsPinned = false,
  onMouseEnter,
  onMouseLeave
}: UseMouseTrackingOptions = {}) {
  const componentRef = useRef<HTMLElement | null>(null);
  const [isMouseOver, setIsMouseOver] = useState(false);
  const [isPinned, setIsPinned] = useState(initialIsPinned);

  const refCallback = useCallback((element: HTMLElement | null) => {
    componentRef.current = element;
  }, []);

  const handleMouseMove = useCallback((event: MouseEvent) => {
    if (!componentRef.current) return;

    const rect = componentRef.current.getBoundingClientRect();
    const isInside =
      event.clientX >= rect.left &&
      event.clientX <= rect.right &&
      event.clientY >= rect.top &&
      event.clientY <= rect.bottom;

    if (isInside !== isMouseOver) {
      setIsMouseOver(isInside);
      if (!isPinned) {
        if (isInside) {
          onMouseEnter?.();
        } else {
          onMouseLeave?.();
        }
      }
    }
  }, [isPinned, isMouseOver, onMouseEnter, onMouseLeave]);

  useEffect(() => {
    document.addEventListener('mousemove', handleMouseMove);
    return () => {
      document.removeEventListener('mousemove', handleMouseMove);
    };
  }, [handleMouseMove]);

  return { ref: refCallback, isMouseOver, isPinned, setIsPinned };
}
