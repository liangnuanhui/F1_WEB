"use client";

export default function HomePage() {
  return (
    <div className="container mx-auto py-8 text-center">
      <h1 className="text-4xl font-bold mb-4">F1 看板</h1>
      <p className="text-xl text-muted-foreground mb-8">
        首页内容正在重新设计中，敬请期待！
      </p>

      {/* 字体测试区域 */}
      <div className="bg-white p-6 rounded-lg shadow-md max-w-2xl mx-auto">
        <h2 className="text-2xl font-bold mb-4">
          Font Test - Formula1 Official Font
        </h2>
        <div className="space-y-4 text-left">
          <p className="text-lg">
            <strong>English Text:</strong> Formula 1 World Championship 2025
          </p>
          <p className="text-lg">
            <strong>Numbers:</strong> 1234567890 - Championship Points: 456.78
          </p>
          <p className="text-lg">
            <strong>Mixed:</strong> 中文混合 English Text 123456 测试字体渲染
          </p>
          <p className="text-lg">
            <strong>Driver Names:</strong> Max Verstappen, Lewis Hamilton, Lando
            Norris
          </p>
          <p className="text-lg">
            <strong>Team Names:</strong> Red Bull Racing, Mercedes-AMG, McLaren
          </p>
          <p className="text-sm">
            Regular weight: The quick brown fox jumps over the lazy dog
          </p>
          <p className="text-sm font-bold">
            Bold weight: The quick brown fox jumps over the lazy dog
          </p>
          <p className="text-xs">
            Small size: Circuit de Monaco, Silverstone Circuit
          </p>
          <p className="text-xl">Large size: FORMULA 1 WORLD CHAMPIONSHIP</p>
        </div>
      </div>
    </div>
  );
}
