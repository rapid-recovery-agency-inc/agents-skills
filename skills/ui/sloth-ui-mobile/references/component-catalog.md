# sloth-ui-mobile Component Catalog

Complete inventory of components exported by `@rapid-recovery-agency-inc/sloth-ui-mobile` v1.222.0.

All imports: `import { ComponentName } from '@rapid-recovery-agency-inc/sloth-ui-mobile';`

## Foundations

### Text

| Export               | Description                                                                              |
| -------------------- | ---------------------------------------------------------------------------------------- |
| `MainText`           | Primary text component. Use for all text rendering. Props: `type`, `themeColor`          |
| `MainTextBase`       | Low-level text component for building reusable components only. Not for screen-level use |
| `MainTextStyle`      | Style constants for all text types                                                       |
| `ResponsiveMainText` | Text with automatic responsive sizing                                                    |
| `NoData`             | Empty state text display                                                                 |
| `VinText`            | Formatted VIN number display                                                             |
| `AddressText`        | Formatted address display                                                                |

**TextType values:** `BLACK_XL8`, `BLACK_XL7`, `BLACK_XL6`, `BLACK_XL5`, `BLACK_XL4`, `BLACK_XL3`, `BLACK_XL2`, `BLACK_XL`, `BLACK_LG`, `BLACK_MD`, `BLACK_SM`, `BLACK_XS`, `BOLD_XL8`...`BOLD_XS`, `BOOK_XL8`...`BOOK_XS`

### Colors & Theming

| Export                  | Description                                                        |
| ----------------------- | ------------------------------------------------------------------ |
| `ThemeProvider`         | Context provider for theme. Wrap app root                          |
| `useTheme`              | Hook returning `{ name, colors, setTheme, isSystemThemeEnabled }`  |
| `useThemeColor`         | Hook returning resolved color for a single token key               |
| `useThemedStyles`       | Hook that resolves theme tokens + responsive breakpoints in styles |
| `createThemeStyleSheet` | Creates a style descriptor with theme token support                |
| `ThemeName`             | Type: `'light' \| 'dark'`                                          |
| `ThemeColorKey`         | Type: union of all theme token names                               |
| `ThemeColorType`        | Type: theme color record                                           |
| `Color`                 | **Deprecated.** Legacy color constants. Use theme tokens           |

### Responsive

| Export                      | Description                                                         |
| --------------------------- | ------------------------------------------------------------------- |
| `DeviceSize`                | Enum: `XS`, `SM`, `MD`, `LG`, `XL`                                  |
| `createResponsiveStyles`    | **Deprecated.** Use `createThemeStyleSheet`                         |
| `useResponsiveStyles`       | **Deprecated.** Use `useThemedStyles`                               |
| `useResponsiveStylesHeight` | Hook for height-based responsive styles                             |
| `selectRenderV2`            | Renders different components for phone (XS/SM) vs tablet (MD/LG/XL) |
| `selectRender`              | **Deprecated.** Use `selectRenderV2`                                |
| `getDeviceSize`             | Returns current `DeviceSize`                                        |
| `isLargeDevice`             | Returns `true` for MD/LG/XL devices                                 |
| `isIos`                     | Platform check constant                                             |

## Atoms

### Buttons

| Export        | Description                                                                                                                    |
| ------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| `Button`      | Current button component. Props: `text`, `size`, `color`, `variant`, `loading`, `disabled`, `leftIcon`, `rightIcon`, `onPress` |
| `MainButton`  | **Deprecated.** Use `Button`                                                                                                   |
| `PlainButton` | **Deprecated.** Use `Button`                                                                                                   |

### Icons

| Export | Description                                                                                                                |
| ------ | -------------------------------------------------------------------------------------------------------------------------- |
| `Icon` | FontAwesome icon component. Props: `iconName`, `size`, `themeColor`, `solid`. **`color` is deprecated** — use `themeColor` |

### Input

| Export       | Description                       |
| ------------ | --------------------------------- |
| `Input`      | Current text input component      |
| `InputField` | Text input with label and styling |
| `DateInput`  | Date input field                  |
| `TimeInput`  | Time input field                  |

### Badge & Pill

| Export             | Description                                        |
| ------------------ | -------------------------------------------------- |
| `BaseBadge`        | Badge component                                    |
| `Pill`             | Status pill/tag. Props: `color`, `variant`, `size` |
| `NotificationPill` | Notification count pill                            |

### Avatar

| Export                | Description                        |
| --------------------- | ---------------------------------- |
| `Avatar`              | User avatar with initials fallback |
| `AvatarRow`           | Row of multiple avatars            |
| `getInitialsFromName` | Utility to extract initials        |

### Checklist & Selection

| Export     | Description             |
| ---------- | ----------------------- |
| `Checkbox` | Checkbox component      |
| `Radio`    | Radio button component  |
| `Toggle`   | Toggle/switch component |

### Divider

| Export      | Description                     |
| ----------- | ------------------------------- |
| `Divider`   | **Deprecated.** Use `DividerV2` |
| `DividerV2` | Updated divider component       |

### Loader

| Export     | Description                    |
| ---------- | ------------------------------ |
| `Loader`   | **Deprecated.** Use `LoaderV2` |
| `LoaderV2` | Updated loading component      |

### Alert

| Export  | Description                                             |
| ------- | ------------------------------------------------------- |
| `Alert` | Alert banner component. Props include `AlertColor` type |

## Molecules

### Tabs

| Export         | Description                |
| -------------- | -------------------------- |
| `BlueTabs`     | Blue-themed tab navigation |
| `FloatingTabs` | Floating tab navigation    |
| `SimpleTabs`   | Minimal tab navigation     |
| `RoundedTab`   | Single rounded tab item    |
| `FloatingTab`  | Single floating tab item   |

### Modals

| Export              | Description                                               |
| ------------------- | --------------------------------------------------------- |
| `BottomSheet`       | **Deprecated.** Use `MainModal` with `mode` prop          |
| `ConfirmationModal` | Confirm/cancel dialog                                     |
| `MainModal`         | General-purpose modal                                     |
| `ModalProvider`     | Modal context provider (already in App.tsx provider tree) |

### Cards

| Export                             | Description                           |
| ---------------------------------- | ------------------------------------- |
| `StatsCardBlue`                    | Blue dashboard stat card              |
| `StatsCardBlueGraph`               | Blue stat card with graph             |
| `StatsCardBlank`                   | Empty/blank stat card                 |
| `StatsCardWhite`                   | White dashboard stat card             |
| `StatsCardWhiteGraph`              | White stat card with graph            |
| `StatsCardWhiteFormatedGraph`      | Formatted white stat card with graph  |
| `StatsCardWhiteFormatedWithButton` | Formatted white stat card with button |
| `getTendencyColor`                 | Utility: color for trend direction    |

### Carousel

| Export         | Description          |
| -------------- | -------------------- |
| `Carousel`     | Horizontal carousel  |
| `GridCarousel` | Grid-layout carousel |

### DatePicker

| Export                                                                                | Description                    |
| ------------------------------------------------------------------------------------- | ------------------------------ |
| `DatePicker`                                                                          | Date range picker component    |
| `useDatePickerStyles`                                                                 | Styles hook for date picker    |
| `getDatepickerRangeDate`                                                              | Utility: calculate date ranges |
| `DateRangeList`, `DateRangeRequired`, `DateRangeOption`, `DateRangeType`, `ViewLabel` | Model types and enums          |
| `DATE_SELECTOR_WIDTH_PHONE`, `DATE_SELECTOR_WIDTH_TABLET`                             | Layout constants               |

### Dropdown

| Export            | Description                  |
| ----------------- | ---------------------------- |
| `Dropdown`        | Standard dropdown            |
| `DropdownRounded` | Rounded variant              |
| `DropdownButton`  | Dropdown trigger button      |
| `BaseDropdown`    | Low-level dropdown component |

### Other

| Export                  | Description                     |
| ----------------------- | ------------------------------- |
| `Growth`                | Growth/trend indicator          |
| `getTendencyFromString` | Utility: parse tendency string  |
| `LeaderboardItem`       | Leaderboard row component       |
| `getRankIcon`           | Utility: icon for rank position |
| `NotesSection`          | Notes display section           |
| `UserDetails`           | User info component with avatar |
| `Container`             | Layout container                |
| `Background`            | Background wrapper component    |

## Figma Design System

Components are mapped to the [Mobile Design System Figma](https://www.figma.com/design/ZSvpk711R1PCVMpfZDLLdB/Design-System---Mobile-App-2025).

When implementing UI, use this document as the primary reference for available components and exports.

Consult the Figma design system for visual specifications only when the agent or user has a working browser or Figma access path.

If Figma is not accessible in the current workflow, rely on the Markdown catalog first and ask the user for missing visual details before building custom components.
