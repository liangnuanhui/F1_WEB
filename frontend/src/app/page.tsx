"use client";

export default function HomePage() {
  return (
    <div className="container mx-auto py-8 text-center">
      <h1 className="text-4xl font-bold mb-4">F1 看板</h1>
      <p className="text-xl text-muted-foreground mb-8">
        首页内容正在重新设计中，敬请期待！
      </p>

      {/* 字体测试区域 */}
      <div className="bg-white p-6 rounded-lg shadow-md max-w-4xl mx-auto">
        <h2 className="text-2xl font-bold mb-6">
          字体测试 - Formula1 + 阿里妈妈数黑体
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* 中文字体测试 */}
          <div className="space-y-4 text-left">
            <h3 className="text-lg font-bold text-blue-600 mb-3">
              中文字体测试 (阿里妈妈数黑体)
            </h3>
            <p className="text-lg">
              <strong>赛事名称：</strong>一级方程式世界锦标赛
            </p>
            <p className="text-lg">
              <strong>车手姓名：</strong>马克斯·维斯塔潘、刘易斯·汉密尔顿
            </p>
            <p className="text-lg">
              <strong>车队名称：</strong>红牛车队、梅赛德斯车队、迈凯伦车队
            </p>
            <p className="text-lg">
              <strong>赛道信息：</strong>摩纳哥赛道、银石赛道、铃鹿赛道
            </p>
            <p className="text-sm">小字号：赛车运动的巅峰竞技</p>
            <p className="text-xl">大字号：一级方程式赛车</p>
            <p className="text-sm font-bold">粗体：速度与激情的完美结合</p>
          </div>

          {/* 英文字体测试 */}
          <div className="space-y-4 text-left">
            <h3 className="text-lg font-bold text-red-600 mb-3">
              English Font Test (Formula1)
            </h3>
            <p className="text-lg">
              <strong>Championship:</strong> Formula 1 World Championship 2025
            </p>
            <p className="text-lg">
              <strong>Driver Names:</strong> Max Verstappen, Lewis Hamilton,
              Lando Norris
            </p>
            <p className="text-lg">
              <strong>Team Names:</strong> Red Bull Racing, Mercedes-AMG,
              McLaren
            </p>
            <p className="text-lg">
              <strong>Circuits:</strong> Circuit de Monaco, Silverstone Circuit
            </p>
            <p className="text-sm">Small size: The pinnacle of motorsport</p>
            <p className="text-xl">Large size: FORMULA 1 RACING</p>
            <p className="text-sm font-bold">
              Bold: Speed and precision combined
            </p>
          </div>
        </div>

        {/* 混合文本测试 */}
        <div className="mt-8 space-y-4 text-left">
          <h3 className="text-lg font-bold text-green-600 mb-3">
            中英文混合测试
          </h3>
          <p className="text-lg">
            <strong>赛程安排：</strong>2025年 Formula 1 赛季将于3月在 Bahrain
            巴林揭幕
          </p>
          <p className="text-lg">
            <strong>积分统计：</strong>Max Verstappen
            马克斯·维斯塔潘目前积分：425分
          </p>
          <p className="text-lg">
            <strong>速度记录：</strong>最高时速 372.5 km/h，创造于 Monza
            蒙扎赛道
          </p>
          <p className="text-lg">
            <strong>车队排名：</strong>Red Bull Racing 红牛车队领跑 2024
            Constructors' Championship
          </p>
          <div className="bg-gray-100 p-4 rounded mt-4">
            <p className="text-sm text-gray-600">
              数字测试：赛车编号 1, 33, 44, 63 | 圈速 1:23.456 | 排位赛 Q1, Q2,
              Q3
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
