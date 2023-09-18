import { Component } from '@angular/core';

@Component({
  selector: 'app-carga-masiva',
  templateUrl: './carga-masiva.component.html',
  styleUrls: ['./carga-masiva.component.css']
})

export class CargaMasivaComponent {

  // Matriz de objetos para mantener datos y encabezados de archivos CSV
  csvDataArray: { fileData: any[][], tableHeaders: string[] }[] = [];

  onFileSelected(event: any): void {
    const file: File = event.target.files[0];
    if (file) {
      this.readFile(file);
    }
  }

  private readFile(file: File): void {
    const reader: FileReader = new FileReader();

    reader.onload = (e: any) => {
      const contents = e.target.result;
      this.parseCSV(contents);
    };

    reader.readAsText(file);
  }

  private parseCSV(contents: string): void {
    const lines = contents.split('\n');
    if (lines.length > 0) {
      const tableHeaders = lines[0].split(',').map(header => header.trim());
      const fileData = lines.slice(1).map(line => {
        const row = [];
        let insideQuotes = false;
        let cell = '';

        for (let i = 0; i < line.length; i++) {
          const char = line.charAt(i);

          if (char === '"') {
            insideQuotes = !insideQuotes;
          } else if (char === ',' && !insideQuotes) {
            // Agrega la celda actual a la fila
            row.push(cell.trim());
            cell = '';
          } else {
            cell += char;
          }
        }

        // Agrega la última celda a la fila
        row.push(cell.trim());
        return row;
      });

      // Agrega los datos y encabezados del archivo CSV como un objeto en la matriz
      this.csvDataArray.push({ fileData, tableHeaders });
    }
  }

}
