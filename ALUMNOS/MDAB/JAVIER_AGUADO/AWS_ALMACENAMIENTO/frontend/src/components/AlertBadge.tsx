import { Badge } from "@/components/ui/badge";

interface Props {
  alert: boolean;
  label: string;
}

export function AlertBadge({ alert, label }: Props) {
  return (
    <Badge variant={alert ? "destructive" : "secondary"}>
      {alert ? "⚠ " : ""}{label}
    </Badge>
  );
}
