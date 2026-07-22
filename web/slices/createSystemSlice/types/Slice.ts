interface Slice {
  // actions
  setSidebarAction: (open: boolean) => void;
  // state
  sidebarOpen: boolean;
}

export default Slice;
