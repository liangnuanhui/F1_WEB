#!/usr/bin/env python3
"""
F1赛道详细信息同步工具 v2.0

改进功能：
- 100%赛道覆盖率
- 智能批量处理
- 详细的错误报告
- 进度追踪
- 数据完整性验证
"""

import asyncio
import argparse
import logging
import sys
import os
from pathlib import Path

# 添加app目录到路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.services.circuit_sync_service_v2 import sync_circuits_main
from app.core.database import get_db
from app.models.circuit import Circuit

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def list_circuits_status():
    """列出所有赛道及其信息状态"""
    try:
        db = next(get_db())
        circuits = db.query(Circuit).all()
        
        print("\n📋 当前数据库中的赛道:")
        print("=" * 80)
        
        complete_count = 0
        incomplete_count = 0
        
        for circuit in circuits:
            # 检查数据完整性
            has_length = circuit.length is not None
            has_first_gp = circuit.first_grand_prix is not None
            has_laps = circuit.typical_lap_count is not None
            has_distance = circuit.race_distance is not None
            has_lap_record = circuit.lap_record is not None
            has_image = circuit.circuit_layout_image_url is not None
            
            # 生成状态图标
            status_icons = []
            if has_length:
                status_icons.append("📏")
            if has_first_gp:
                status_icons.append("🏁")
            if has_laps:
                status_icons.append("🔄")
            if has_distance:
                status_icons.append("📐")
            if has_lap_record:
                status_icons.append("⏱️")
            if has_image:
                status_icons.append("🖼️")
            
            status_str = "".join(status_icons) if status_icons else "❌"
            
            if len(status_icons) >= 5:  # 认为基本完整（至少有5个主要字段）
                complete_count += 1
            else:
                incomplete_count += 1
            
            print(f"{circuit.circuit_id:15} | {circuit.circuit_name:30} | {circuit.country:15} | {status_str}")
        
        print("=" * 80)
        print("📏 赛道长度 | 🏁 首次GP+圈数 | 📐 比赛距离 | ⏱️ 圈速记录 | 🖼️ 布局图")
        print(f"\n📊 统计: 完整 {complete_count}, 不完整 {incomplete_count}, 总计 {len(circuits)}")
        
        db.close()
        
    except Exception as e:
        logger.error(f"❌ 列出赛道状态失败: {e}")


async def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="F1赛道详细信息同步工具 v2.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  python sync_circuit_details_v2.py                          # 只同步缺失信息的赛道
  python sync_circuit_details_v2.py --all                    # 强制同步所有赛道
  python sync_circuit_details_v2.py --circuits spa silverstone # 同步指定赛道
  python sync_circuit_details_v2.py --list                   # 列出所有赛道状态
  python sync_circuit_details_v2.py --test                   # 测试少量赛道
  python sync_circuit_details_v2.py --delay 5                # 自定义请求间隔
        """
    )
    
    # 命令选项
    parser.add_argument('--all', action='store_true', 
                       help='强制同步所有赛道（即使已有信息）')
    parser.add_argument('--circuits', nargs='+', metavar='CIRCUIT_ID',
                       help='指定要同步的赛道ID列表')
    parser.add_argument('--list', action='store_true',
                       help='列出所有赛道及其信息状态')
    parser.add_argument('--test', action='store_true',
                       help='测试模式：只同步3个赛道用于验证')
    parser.add_argument('--delay', type=float, default=3.0, metavar='SECONDS',
                       help='请求间延迟秒数 (默认: 3.0)')
    
    args = parser.parse_args()
    
    # 列出赛道状态
    if args.list:
        list_circuits_status()
        return
    
    # 准备同步参数
    circuit_ids = None
    force_update = False
    missing_only = True  # 默认只同步缺失的
    
    if args.test:
        logger.info("🧪 运行在测试模式")
        circuit_ids = ["spa", "silverstone", "monaco"]
        force_update = True
        missing_only = False
    elif args.all:
        logger.info("🎯 强制同步所有赛道")
        force_update = True
        missing_only = False
    elif args.circuits:
        logger.info(f"🎯 同步指定赛道: {args.circuits}")
        circuit_ids = args.circuits
        force_update = True
        missing_only = False
    else:
        logger.info("🎯 智能模式：只同步缺失信息的赛道")
    
    # 显示同步前状态
    logger.info("📊 同步前状态:")
    list_circuits_status()
    
    # 执行同步
    logger.info("\n🚀 开始F1赛道信息同步...")
    
    try:
        result = await sync_circuits_main(
            circuit_ids=circuit_ids,
            force_update=force_update,
            missing_only=missing_only,
            delay_between_requests=args.delay
        )
        
        # 判断整体结果
        if result.failed == 0:
            logger.info("🎉 所有赛道同步成功!")
        elif result.successful > 0:
            logger.warning(f"⚠️ 部分成功: 成功{result.successful}, 失败{result.failed}")
        else:
            logger.error("💥 同步失败!")
            sys.exit(1)
        
        # 显示同步后状态
        if result.successful > 0:
            logger.info("\n📊 同步后状态:")
            list_circuits_status()
        
    except KeyboardInterrupt:
        logger.info("\n⏸️ 用户中断同步")
        sys.exit(1)
    except Exception as e:
        logger.error(f"💥 同步过程中发生异常: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main()) 