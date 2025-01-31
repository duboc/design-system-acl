import React, { useEffect } from 'react';
import './Dialog.css';
import Button from './Button';

interface DialogProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  children: React.ReactNode;
  variant?: 'default' | 'info' | 'warning' | 'error';
  size?: 'small' | 'medium' | 'large';
  showCloseButton?: boolean;
  actions?: React.ReactNode;
}

export const Dialog: React.FC<DialogProps> = ({
  isOpen,
  onClose,
  title,
  children,
  variant = 'default',
  size = 'medium',
  showCloseButton = true,
  actions,
}) => {
  useEffect(() => {
    const handleEscape = (event: KeyboardEvent) => {
      if (event.key === 'Escape' && isOpen) {
        onClose();
      }
    };

    if (isOpen) {
      document.addEventListener('keydown', handleEscape);
      document.body.style.overflow = 'hidden';
    }

    return () => {
      document.removeEventListener('keydown', handleEscape);
      document.body.style.overflow = 'unset';
    };
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return (
    <>
      <div className="dialog-overlay" onClick={onClose} />
      <div className={`dialog dialog--${variant} dialog--${size}`} role="dialog" aria-modal="true">
        <div className="dialog__header">
          <h2 className="dialog__title">{title}</h2>
          {showCloseButton && (
            <button className="dialog__close" onClick={onClose} aria-label="Close">
              ×
            </button>
          )}
        </div>
        <div className="dialog__content">
          {children}
        </div>
        {actions && (
          <div className="dialog__actions">
            {actions}
          </div>
        )}
      </div>
    </>
  );
};

export default Dialog; 