import { TestBed } from '@angular/core/testing';

import { CargaMasivaService } from './carga-masiva.service';

describe('CargaMasivaService', () => {
  let service: CargaMasivaService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(CargaMasivaService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
