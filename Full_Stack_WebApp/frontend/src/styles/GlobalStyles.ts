import styled, { createGlobalStyle } from "styled-components";

export const GlobalStyle = createGlobalStyle`
  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }

  /* Custom Scrollbar Styling */
  ::-webkit-scrollbar {
    width: 8px;
    height: 8px;
  }

  ::-webkit-scrollbar-track {
    background: rgba(30, 30, 40, 0.3);
    border-radius: 10px;
    border: 1px solid rgba(139, 92, 246, 0.1);
  }

  ::-webkit-scrollbar-thumb {
    background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
    border-radius: 10px;
    border: 1px solid rgba(139, 92, 246, 0.2);
    box-shadow: 0 2px 6px rgba(139, 92, 246, 0.3);
    transition: all 0.3s ease;
  }

  ::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%);
    box-shadow: 0 4px 12px rgba(139, 92, 246, 0.5);
    transform: scale(1.1);
  }

  ::-webkit-scrollbar-thumb:active {
    background: linear-gradient(135deg, #6d28d9 0%, #5b21b6 100%);
  }

  ::-webkit-scrollbar-corner {
    background: rgba(30, 30, 40, 0.3);
  }

  /* Firefox Scrollbar */
  * {
    scrollbar-width: thin;
    scrollbar-color: #8b5cf6 rgba(30, 30, 40, 0.3);
  }

  body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
      'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
      sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    background: linear-gradient(135deg, #0f0f14 0%, #1a1a24 100%);
    color: #ffffff;
    line-height: 1.6;
    min-height: 100vh;
  }

  code {
    font-family: source-code-pro, Menlo, Monaco, Consolas, 'Courier New',
      monospace;
  }

  a {
    color: inherit;
    text-decoration: none;
  }

  button {
    cursor: pointer;
    border: none;
    outline: none;
  }

  input, textarea {
    outline: none;
  }
`;

// SofaScore Theme Colors
export const theme = {
  colors: {
    // Enhanced background colors with better contrast
    primary: "#0f0f14", // Deep dark primary
    secondary: "#1e1e28", // Rich dark secondary
    tertiary: "#2a2a3a", // Elevated surfaces
    quaternary: "#363648", // Hover states

    // Accent colors - more vibrant
    purple: "#7c3aed", // Primary purple
    purpleLight: "#a855f7", // Light purple
    purpleDark: "#6d28d9", // Dark purple
    purpleGlow: "#8b5cf6", // Glowing purple

    // Status colors - enhanced
    green: "#10b981", // Success/win
    greenLight: "#34d399", // Light green
    red: "#ef4444", // Error/loss
    redLight: "#f87171", // Light red
    yellow: "#f59e0b", // Warning/draw
    yellowLight: "#fbbf24", // Light yellow
    blue: "#3b82f6", // Info
    blueLight: "#60a5fa", // Light blue

    // Text colors - improved hierarchy
    textPrimary: "#ffffff", // Primary text
    textSecondary: "#d1d5db", // Secondary text
    textTertiary: "#9ca3af", // Muted text
    textQuaternary: "#6b7280", // Very muted text

    // Border colors - enhanced depth
    border: "#374151", // Default borders
    borderLight: "#4b5563", // Light borders
    borderAccent: "#7c3aed", // Accent borders

    // Special effects
    gradient: {
      primary: "linear-gradient(135deg, #7c3aed 0%, #a855f7 50%, #8b5cf6 100%)",
      secondary: "linear-gradient(135deg, #1e1e28 0%, #2a2a3a 100%)",
      success: "linear-gradient(135deg, #10b981 0%, #34d399 100%)",
      danger: "linear-gradient(135deg, #ef4444 0%, #f87171 100%)",
    },
  },

  breakpoints: {
    mobile: "768px",
    tablet: "1024px",
    desktop: "1200px",
  },

  spacing: {
    xs: "4px",
    sm: "8px",
    md: "16px",
    lg: "24px",
    xl: "32px",
    xxl: "48px",
  },

  borderRadius: {
    sm: "4px",
    md: "8px",
    lg: "12px",
    xl: "16px",
  },

  shadows: {
    sm: "0 1px 2px 0 rgba(0, 0, 0, 0.05)",
    md: "0 4px 6px -1px rgba(0, 0, 0, 0.1)",
    lg: "0 10px 15px -3px rgba(0, 0, 0, 0.1)",
    xl: "0 20px 25px -5px rgba(0, 0, 0, 0.1)",
  },
};

// 12-Column Grid System
export const GridContainer = styled.div`
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 ${theme.spacing.xl};

  /* Responsive padding */
  @media (max-width: ${theme.breakpoints.desktop}) {
    padding: 0 ${theme.spacing.lg};
  }

  @media (max-width: ${theme.breakpoints.tablet}) {
    padding: 0 ${theme.spacing.md};
  }

  @media (max-width: ${theme.breakpoints.mobile}) {
    padding: 0 ${theme.spacing.sm};
  }
`;

export const GridRow = styled.div`
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: ${theme.spacing.lg};

  @media (max-width: ${theme.breakpoints.tablet}) {
    gap: ${theme.spacing.md};
  }

  @media (max-width: ${theme.breakpoints.mobile}) {
    gap: ${theme.spacing.sm};
  }
`;

export const GridCol = styled.div<{
  span?: number;
  spanTablet?: number;
  spanMobile?: number;
}>`
  grid-column: span ${(props) => props.span || 12};

  @media (max-width: ${theme.breakpoints.tablet}) {
    grid-column: span ${(props) => props.spanTablet || props.span || 12};
  }

  @media (max-width: ${theme.breakpoints.mobile}) {
    grid-column: span ${(props) => props.spanMobile || 12};
  }
`;

// Common styled components
export const Container = styled.div`
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 ${theme.spacing.xl};

  /* Responsive padding to match the 12-column system */
  @media (max-width: ${theme.breakpoints.desktop}) {
    padding: 0 ${theme.spacing.lg};
  }

  @media (max-width: ${theme.breakpoints.tablet}) {
    padding: 0 ${theme.spacing.md};
  }

  @media (max-width: ${theme.breakpoints.mobile}) {
    padding: 0 ${theme.spacing.sm};
  }
`;

export const Card = styled.div`
  background: ${theme.colors.secondary};
  border-radius: ${theme.borderRadius.lg};
  padding: ${theme.spacing.lg};
  border: 1px solid ${theme.colors.border};

  &:hover {
    background: ${theme.colors.tertiary};
    transition: background-color 0.2s ease;
  }
`;

export const Button = styled.button<{
  variant?: "primary" | "secondary" | "outline";
}>`
  padding: ${theme.spacing.sm} ${theme.spacing.md};
  border-radius: ${theme.borderRadius.md};
  font-weight: 500;
  font-size: 14px;
  transition: all 0.2s ease;

  ${(props) => {
    switch (props.variant) {
      case "primary":
        return `
          background: ${theme.colors.purple};
          color: white;
          &:hover {
            background: ${theme.colors.purpleDark};
          }
        `;
      case "secondary":
        return `
          background: ${theme.colors.secondary};
          color: ${theme.colors.textPrimary};
          border: 1px solid ${theme.colors.border};
          &:hover {
            background: ${theme.colors.tertiary};
          }
        `;
      case "outline":
        return `
          background: transparent;
          color: ${theme.colors.purple};
          border: 1px solid ${theme.colors.purple};
          &:hover {
            background: ${theme.colors.purple};
            color: white;
          }
        `;
      default:
        return `
          background: ${theme.colors.purple};
          color: white;
          &:hover {
            background: ${theme.colors.purpleDark};
          }
        `;
    }
  }}
`;

export const Flex = styled.div.withConfig({
  shouldForwardProp: (prop) =>
    !["direction", "justify", "align", "gap", "wrap"].includes(prop),
})<{
  direction?: "row" | "column";
  justify?:
    | "flex-start"
    | "center"
    | "flex-end"
    | "space-between"
    | "space-around";
  align?: "flex-start" | "center" | "flex-end" | "stretch";
  gap?: string;
  wrap?: "wrap" | "nowrap";
}>`
  display: flex;
  flex-direction: ${(props) => props.direction || "row"};
  justify-content: ${(props) => props.justify || "flex-start"};
  align-items: ${(props) => props.align || "stretch"};
  gap: ${(props) => props.gap || "0"};
  flex-wrap: ${(props) => props.wrap || "nowrap"};
`;

export const Grid = styled.div.withConfig({
  shouldForwardProp: (prop) => !["columns", "gap"].includes(prop),
})<{ columns?: number; gap?: string }>`
  display: grid;
  grid-template-columns: repeat(${(props) => props.columns || 1}, 1fr);
  gap: ${(props) => props.gap || theme.spacing.md};
`;

export const Text = styled.span.withConfig({
  shouldForwardProp: (prop) => !["size", "weight", "color"].includes(prop),
})<{
  size?: "xs" | "sm" | "md" | "lg" | "xl";
  weight?: "normal" | "medium" | "semibold" | "bold";
  color?:
    | "primary"
    | "secondary"
    | "tertiary"
    | "purple"
    | "green"
    | "red"
    | "yellow";
}>`
  font-size: ${(props) => {
    switch (props.size) {
      case "xs":
        return "12px";
      case "sm":
        return "14px";
      case "md":
        return "16px";
      case "lg":
        return "18px";
      case "xl":
        return "24px";
      default:
        return "16px";
    }
  }};

  font-weight: ${(props) => {
    switch (props.weight) {
      case "normal":
        return "400";
      case "medium":
        return "500";
      case "semibold":
        return "600";
      case "bold":
        return "700";
      default:
        return "400";
    }
  }};

  color: ${(props) => {
    switch (props.color) {
      case "primary":
        return theme.colors.textPrimary;
      case "secondary":
        return theme.colors.textSecondary;
      case "tertiary":
        return theme.colors.textTertiary;
      case "purple":
        return theme.colors.purple;
      case "green":
        return theme.colors.green;
      case "red":
        return theme.colors.red;
      case "yellow":
        return theme.colors.yellow;
      default:
        return theme.colors.textPrimary;
    }
  }};
`;
