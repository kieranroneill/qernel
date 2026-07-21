import { BuildWorkspace } from '@/components/builds/BuildWorkspace';

interface BuildPageProps {
  params: Promise<{
    id: string;
  }>;
}

export default async function BuildPage({ params }: BuildPageProps) {
  const { id } = await params;

  return <BuildWorkspace buildId={id} />;
}
