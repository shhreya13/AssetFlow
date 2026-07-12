function Navbar() {
  return (
    <header className="h-16 bg-white shadow flex items-center justify-between px-8">
      <h1 className="text-2xl font-semibold text-slate-700">
        AssetFlow Dashboard
      </h1>

      <div className="flex items-center gap-3">
        <div className="w-10 h-10 rounded-full bg-blue-600 text-white flex items-center justify-center font-bold">
          D
        </div>

        <div>
          <p className="font-semibold">Dharshini</p>
          <p className="text-sm text-gray-500">Asset Manager</p>
        </div>
      </div>
    </header>
  );
}

export default Navbar;