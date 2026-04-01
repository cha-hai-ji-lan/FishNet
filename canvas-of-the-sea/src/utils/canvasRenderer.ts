// ... existing code ...

class CanvasRenderer {
  private canvas: HTMLCanvasElement | null = null
  private ctx: CanvasRenderingContext2D | null = null
  

  constructor(canvasId?: string) {
    if (canvasId) {
      this.init(canvasId)
    }
  }

  init(canvasId: string): boolean {
    this.canvas = document.getElementById(canvasId) as HTMLCanvasElement
    if (!this.canvas) {
      console.error(`未找到 id 为 "${canvasId}" 的 canvas 元素`)
      return false
    }
    
    const computedStyle = window.getComputedStyle(this.canvas)
    if (computedStyle.height === 'auto' || computedStyle.height === '') {
      const parent = this.canvas.parentElement
      if (parent) {
        const parentStyle = window.getComputedStyle(parent)
        this.canvas.style.height = parentStyle.height
        this.canvas.style.width = parentStyle.width
      } else {
        this.canvas.style.height = '100vh'
        this.canvas.style.width = '100vw'
      }
    }
    
    this.ctx = this.canvas.getContext('2d')
    if (!this.ctx) {
      console.error('无法获取 2D 渲染上下文')
      return false
    }

    return true
  }

  resize() {
    if (!this.canvas || !this.ctx) return
    
    const rect = this.canvas.getBoundingClientRect()
    
    if (rect.width === 0 || rect.height === 0) {
      console.warn('Canvas 尺寸为 0 跳过 resize')
      return
    }
    
    this.canvas.width = rect.width
    this.canvas.height = rect.height
    console.log(this.canvas.width, this.canvas.height)
    this.ctx.scale(window.devicePixelRatio, window.devicePixelRatio)
    this.ctx.translate(this.canvas.width / 2, this.canvas.height / 2)
    
  }

  clear() {
    if (!this.ctx || !this.canvas) return
    this.ctx.clearRect(0, 0, this.canvas.width / window.devicePixelRatio, this.canvas.height / window.devicePixelRatio)
  }

  drawline(){
    if (this.ctx) {
      this.ctx.beginPath()           // 开始路径
      this.ctx.moveTo(0, 0)         // 移动到起点 (0,0)
      this.ctx.lineTo(10, 10)       // 绘制到终点 (10,10)
      this.ctx.strokeStyle = '#000000'  // 设置线条颜色（黑色）
      this.ctx.lineWidth = 1        // 设置线条宽度
      this.ctx.stroke()             // 绘制路径
    }
  }

}

export const canvasRenderer = new CanvasRenderer()
export default CanvasRenderer