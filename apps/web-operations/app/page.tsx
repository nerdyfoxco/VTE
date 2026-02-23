import { redirect } from 'next/navigation';

export default function Home() {
  // Enforce zero-friction routing directly into the active Work Queue.
  redirect('/queue');
}
