#!/usr/bin/env python
"""
F1赛道详细信息同步脚本

用法:
  python sync_circuit_details.py                    # 同步所有缺少信息的赛道
  python sync_circuit_details.py --all             # 强制同步所有赛道
  python sync_circuit_details.py --circuits spa silverstone  # 同步指定赛道
"""

import asyncio
import argparse
import sys
import os

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import get_db
from app.services.circuit_sync_service import sync_circuits_main
from app.models.circuit import Circuit
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('circuit_sync.log')
    ]
)

logger = logging.getLogger(__name__)


def list_circuits():
    """列出所有赛道"""
    db = next(get_db())
    try:
        circuits = db.query(Circuit).all()
        print("\n📋 当前数据库中的赛道:")
        print("=" * 80)
        
        for circuit in circuits:
            status_icons = []
            if circuit.length:
                status_icons.append("📏")  # 有长度信息
            if circuit.first_grand_prix:
                status_icons.append("🏁")  # 有首次GP信息
            if circuit.lap_record:
                status_icons.append("⏱️")   # 有圈速记录
            if circuit.circuit_layout_image_url:
                status_icons.append("🖼️")   # 有布局图
            
            status = "".join(status_icons) if status_icons else "❌"
            print(f"{circuit.circuit_id:15} | {circuit.circuit_name:30} | {circuit.country:15} | {status}")
        
        print("=" * 80)
        print("📏 赛道长度 | 🏁 首次GP | ⏱️ 圈速记录 | 🖼️ 布局图")
        
    finally:
        db.close()


async def main():
    parser = argparse.ArgumentParser(
        description="F1赛道详细信息同步工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python sync_circuit_details.py                     # 同步缺少信息的赛道
  python sync_circuit_details.py --all              # 强制同步所有赛道
  python sync_circuit_details.py --circuits spa silverstone  # 同步指定赛道
  python sync_circuit_details.py --list             # 列出所有赛道
        """
    )
    
    parser.add_argument(
        '--all', 
        action='store_true',
        help='强制同步所有赛道（即使已有信息）'
    )
    
    parser.add_argument(
        '--circuits',
        nargs='+',
        help='指定要同步的赛道ID列表'
    )
    
    parser.add_argument(
        '--list',
        action='store_true',
        help='列出所有赛道及其信息状态'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='预演模式，不实际执行同步'
    )
    
    args = parser.parse_args()
    
    if args.list:
        list_circuits()
        return
    
    if args.dry_run:
        logger.info("🧪 运行在预演模式，不会实际同步数据")
        # 这里可以添加预演逻辑
        return
    
    logger.info("🚀 开始F1赛道信息同步...")
    
    try:
        if args.circuits:
            # 同步指定赛道
            logger.info(f"🎯 同步指定赛道: {args.circuits}")
            results = await sync_circuits_main(circuit_ids=args.circuits)
        else:
            # 同步所有赛道
            logger.info(f"🔄 {'强制' if args.all else '增量'}同步所有赛道")
            results = await sync_circuits_main(force_update=args.all)
        
        # 输出结果
        print("\n" + "=" * 50)
        print("📊 同步结果汇总")
        print("=" * 50)
        
        for key, value in results.items():
            if key == "missing" and value:
                print(f"❌ {key}: {value}")
            else:
                print(f"📈 {key}: {value}")
        
        print("=" * 50)
        
        # 检查结果
        if results.get("failed", 0) > 0:
            logger.warning(f"⚠️ {results['failed']} 个赛道同步失败，请检查日志")
            sys.exit(1)
        else:
            logger.info("🎉 所有赛道同步成功!")
    
    except Exception as e:
        logger.error(f"❌ 同步过程出现错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main()) 