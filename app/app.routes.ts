import { provideRouter, RouterConfig }  from '@angular/router';
import { HeroesComponent } from './heroes.component';
import {DashboardComponent} from './dashboard.component';
import { HeroDetailComponent } from './hero-detail.component';
import { MapComponent } from './map.component';
import { ChartComponent} from './chart.component';

const routes: RouterConfig = [
  {
    path: 'heroes',
    component: HeroesComponent
  },
  {
    path: 'dashboard',
    component: DashboardComponent
  },
  {
    path: '',
    redirectTo: '/dashboard',
    pathMatch: 'full'
  },
  {
  path: 'detail/:id',
  component: HeroDetailComponent
  },
  {
  path: 'map',
  component: MapComponent
  },
  {
  path: 'charts',
  component: ChartComponent
  },  
];

export const APP_ROUTER_PROVIDERS = [
  provideRouter(routes)
];
