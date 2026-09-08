import { LoginForm } from '@/features/auth/components/LoginForm'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/shared/components/ui/card'

export function LoginPage() {
  return (
    <div className="bg-muted/40 flex min-h-svh items-center justify-center p-4">
      <Card className="w-full max-w-sm">
        <CardHeader>
          <CardTitle className="text-xl">Nexus</CardTitle>
          <CardDescription>Sign in to the Enterprise Asset &amp; Compliance Management System</CardDescription>
        </CardHeader>
        <CardContent>
          <LoginForm />
          <p className="text-muted-foreground mt-6 text-center text-xs">
            Seed accounts: admin@nexus.io · manager@nexus.io · viewer@nexus.io
            <br />
            Password: ChangeMe123!
          </p>
        </CardContent>
      </Card>
    </div>
  )
}
