import { ref } from "vue";
export const CR = ref<CanvasRenderer | null>(null)

class CanvasRenderer {
  private canvas: HTMLCanvasElement | null = null
  private ctx: CanvasRenderingContext2D | null = null
  private canvas_type: string = "__NULL__"


  constructor(canvasId: string) {
    this.init(canvasId)
  }

  init(canvasId: string): boolean {
    this.canvas_type = canvasId
    this.canvas = document.getElementById(canvasId) as HTMLCanvasElement
    this.ctx = this.canvas.getContext('2d')

    return false
  }

  set_canvas_size(states: boolean) {
    if (!this.canvas) return
    if (states) {
      switch (this.canvas_type) {
        case 'two-piece-canvas':
          this.canvas.style.width = "40vmin"
          this.canvas.style.height = "100%"
          console.log(this.canvas.style.width)
          console.log(this.canvas.style.height)
          break;

        default:
          break;
      }
    } else {
      this.canvas.style.width = ""
      this.canvas.style.height = ""
    }
  }
}

export const canvasRenderer = (type: string) => {
  CR.value = new CanvasRenderer(type)
}
export default CanvasRenderer