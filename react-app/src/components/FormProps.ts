import { FormEvent, ReactNode } from 'react';

export interface FormProps {
  children: ReactNode;
  variant?: 'primary' | 'secondary';
  size?: 'small' | 'medium' | 'large';
  onSubmit?: (event: FormEvent<HTMLFormElement>) => void;
} 