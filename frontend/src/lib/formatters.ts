/**
 * 格式化工具函数集合
 * 统一管理前端数据格式化逻辑
 */

/**
 * 格式化车手姓名用于图片文件名
 * 移除重音符号并将空格替换为下划线
 * @param name 车手姓名
 * @returns 格式化后的文件名
 */
export const formatNameForImage = (name: string): string => {
  return name
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/ /g, "_");
};

/**
 * 格式化车手姓名用于头像查找
 * 规范化特殊字符并替换空格为下划线
 * @param driverName 车手姓名
 * @returns 格式化后的头像文件名
 */
export const formatAvatarName = (driverName: string): string => {
  // 规范化处理特殊字符 (如 ü -> u) 并替换空格为下划线
  const normalizedName = driverName
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "");
  return normalizedName.replace(/ /g, "_");
};

/**
 * 分割车手姓名用于显示格式化
 * @param driverName 车手姓名
 * @returns 包含firstName和lastName的对象，用于组件中的显示格式化
 */
export const formatDriverDisplayName = (driverName: string) => {
  const parts = driverName.split(" ");
  if (parts.length > 1) {
    const firstName = parts.slice(0, -1).join(" ");
    const lastName = parts[parts.length - 1];
    return { firstName, lastName };
  }
  return { firstName: "", lastName: driverName };
};

/**
 * 分割车手姓名为名字和姓氏
 * @param driverName 车手姓名
 * @returns 包含firstName和lastName的对象
 */
export const splitDriverName = (driverName: string) => {
  const [firstName, ...lastNameParts] = driverName.split(" ");
  const lastName = lastNameParts.join(" ");
  return { firstName, lastName };
}; 